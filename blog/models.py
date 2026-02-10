
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# ==============================
# CATEGORY MODEL
# ==============================
class Category(models.Model):
    name_en = models.CharField(max_length=200)
    name_sw = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name_en

    def get_absolute_url(self):
        return reverse("category_posts", args=[self.slug])


# ==============================
# TAG MODEL
# ==============================
class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


# ==============================
# POST MODEL (Bilingual + Dynamic Monetization)
# ==============================
class Post(models.Model):
    POST_TYPE_CHOICES = [
        ("course", "Course"),
        ("book", "Book"),
        ("product", "Product"),
        ("service", "Service"),
        ("free", "Free Resource"),
        ("external", "External Link"),
    ]

    CTA_CHOICES = [
        ("enroll", "Enroll Now"),
        ("buy", "Buy Now"),
        ("pay", "Pay Now"),
        ("download", "Download"),
        ("visit", "Visit Link"),
        ("none", "No CTA"),
    ]

    title_en = models.CharField(max_length=255)
    title_sw = models.CharField(max_length=255, blank=True, null=True)

    slug = models.SlugField(unique=True)

    content_en = models.TextField()
    content_sw = models.TextField(blank=True, null=True)

    meta_description_en = models.TextField(blank=True, null=True)
    meta_description_sw = models.TextField(blank=True, null=True)

    category = models.ForeignKey(Category, related_name="posts", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    featured_image = models.ImageField(upload_to="posts/", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # ===== Dynamic Monetization Fields =====
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default="course")
    cta_text = models.CharField(max_length=50, choices=CTA_CHOICES, default="enroll")
    cta_link = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title_en

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])


# ==============================
# COMMENT MODEL (Replies Supported)
# ==============================
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    # Logged-in users
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Guests
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    content = models.TextField()

    # Parent comment (for replies)
    parent = models.ForeignKey(
        "self",
        related_name="replies",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    likes = models.PositiveIntegerField(default=0)
    approved = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or self.user} - {self.post}"


# ==============================
# SUBSCRIBER MODEL
# ==============================
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
