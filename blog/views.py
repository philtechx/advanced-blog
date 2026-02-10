
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Count, F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import translate_url

from .models import Post, Category, Subscriber, Comment


# ==================================================
# LANGUAGE HELPER
# ==================================================
def get_lang(request):
    return getattr(request, "LANGUAGE_CODE", "en")


# ==================================================
# SIDEBAR CONTEXT (Categories + Popular Posts)
# ==================================================
def get_sidebar_context():
    categories = []
    for category in Category.objects.annotate(post_count=Count("posts")):
        first_post = category.posts.filter(is_published=True).order_by("created").first()
        if first_post:
            categories.append({
                "category": category,
                "first_post": first_post,
                "count": category.posts.filter(is_published=True).count()
            })
    popular_posts = Post.objects.filter(is_published=True).order_by("-views")[:5]
    return {"categories": categories, "popular_posts": popular_posts}


# ==================================================
# HOME PAGE — POST LIST
# ==================================================
def post_list(request):
    lang = get_lang(request)
    posts = Post.objects.filter(is_published=True).select_related("category", "author")
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {"posts": page_obj, "lang": lang}
    context.update(get_sidebar_context())
    return render(request, "post_list.html", context)


# ==================================================
# POST DETAIL — COMMENTS + REPLIES + CTA
# ==================================================
def post_detail(request, slug):
    lang = get_lang(request)
    post = get_object_or_404(Post, slug=slug, is_published=True)

    # Increment views
    post.views += 1
    post.save(update_fields=["views"])

    # Parent comments only
    comments = post.comments.filter(parent__isnull=True, approved=True).order_by("-created")

    # Handle comment submission
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        parent_id = request.POST.get("parent")

        if content:
            parent_comment = None
            # Replying to a comment
            if parent_id:
                parent_comment = Comment.objects.filter(id=parent_id, post=post).first()
                # Guests cannot reply
                if parent_comment and not request.user.is_authenticated:
                    messages.error(request, _("Login required to reply"))
                    return redirect(post.get_absolute_url())

            # Logged-in user
            if request.user.is_authenticated:
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    content=content,
                    parent=parent_comment
                )
            # Guest user
            else:
                name = request.POST.get("name", "").strip()
                email = request.POST.get("email", "").strip()
                if parent_comment:
                    messages.error(request, _("Guests cannot reply"))
                    return redirect(post.get_absolute_url())
                if not name or not email:
                    messages.error(request, _("Name and email required"))
                    return redirect(post.get_absolute_url())
                Comment.objects.create(
                    post=post,
                    name=name,
                    email=email,
                    content=content
                )
            messages.success(request, _("Comment posted successfully!"))
            return redirect(post.get_absolute_url())

    context = {
        "post": post,
        "comments": comments,
        "lang": lang,
        # Pass CTA dynamically to template
        "cta_text": post.get_cta_text_display() if post.cta_text else None,
        "cta_link": post.cta_link,
        "price": post.price,
        "instructions": post.instructions
    }
    context.update(get_sidebar_context())
    return render(request, "post_detail.html", context)


# ==================================================
# CATEGORY POSTS
# ==================================================
def category_posts(request, slug):
    lang = get_lang(request)
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(is_published=True)
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {"category": category, "posts": page_obj, "lang": lang}
    context.update(get_sidebar_context())
    return render(request, "category_posts.html", context)


# ==================================================
# SEARCH (BILINGUAL)
# ==================================================
def search(request):
    lang = get_lang(request)
    query = request.GET.get("q", "").strip()
    results = Post.objects.filter(is_published=True)
    if query:
        results = results.filter(
            Q(title_en__icontains=query) |
            Q(title_sw__icontains=query) |
            Q(content_en__icontains=query) |
            Q(content_sw__icontains=query)
        )
    paginator = Paginator(results, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {"results": page_obj, "query": query, "lang": lang}
    context.update(get_sidebar_context())
    return render(request, "search_results.html", context)


# ==================================================
# REGISTER USER
# ==================================================
def register(request):
    lang = get_lang(request)
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, _("Passwords do not match"))
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, _("Username already exists"))
            return redirect("register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, _("Account created successfully"))
        return redirect("home")
    return render(request, "auth/register.html", {"lang": lang})


# ==================================================
# LOGIN USER
# ==================================================
def user_login(request):
    lang = get_lang(request)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, _("Welcome back!"))
            return redirect("home")
        messages.error(request, _("Invalid credentials"))
    return render(request, "auth/login.html", {"lang": lang})


# ==================================================
# LOGOUT USER
# ==================================================
def user_logout(request):
    logout(request)
    messages.success(request, _("Logged out"))
    return redirect("home")


# ==================================================
# LIKE COMMENT
# ==================================================
def like_comment(request, comment_id):
    Comment.objects.filter(id=comment_id).update(likes=F("likes") + 1)
    return redirect(request.META.get("HTTP_REFERER", "/"))


# ==================================================
# SUBSCRIBE
# ==================================================
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, _("Already subscribed"))
        else:
            Subscriber.objects.create(email=email)
            messages.success(request, _("Subscribed successfully"))
    return redirect(request.META.get("HTTP_REFERER", "/"))


# ==================================================
# STATIC PAGES
# ==================================================
def about(request):
    lang = get_lang(request)
    context = {"lang": lang}
    context.update(get_sidebar_context())
    return render(request, "about.html", context)


def contact(request):
    lang = get_lang(request)
    context = {"lang": lang}
    context.update(get_sidebar_context())
    if request.method == "POST":
        messages.success(request, _("Message sent"))
    return render(request, "contact.html", context)


# ==================================================
# LANGUAGE SWITCH
# ==================================================
@require_POST
def set_language(request):
    lang_code = request.POST.get("language")
    if lang_code in dict(settings.LANGUAGES):
        next_url = request.POST.get("next", request.META.get("HTTP_REFERER", "/"))
        return HttpResponseRedirect(translate_url(next_url, lang_code))
    return redirect("/")
