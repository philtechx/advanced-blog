from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from . import views

urlpatterns = [
    path("set-language/", views.set_language, name="set_language"),
]

urlpatterns += i18n_patterns(
    path("", views.post_list, name="home"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>/", views.category_posts, name="category_posts"),
    path("search/", views.search, name="search"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("comment/like/<int:comment_id>/", views.like_comment, name="like_comment"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
)
