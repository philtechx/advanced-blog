# blog/admin.py
from django.contrib import admin
from .models import Post, Category, Tag, Subscriber, Comment

# ----------------------------------
# Category Admin
# ----------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_sw', 'slug']
    prepopulated_fields = {'slug': ('name_en',)}

# ----------------------------------
# Post Admin (Updated with Monetization CTA)
# ----------------------------------
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title_en',
        'title_sw',
        'author',
        'category',
        'created',
        'views',
        'is_published',
        'is_featured',
        'cta_text',      # CTA button text
        'cta_link',      # CTA link
        'price',         # Optional price
    ]
    list_filter = ['category', 'created', 'is_published', 'is_featured']
    search_fields = [
        'title_en', 'title_sw',
        'content_en', 'content_sw',
        'meta_description_en', 'meta_description_sw',
        'cta_text', 'cta_link'
    ]
    ordering = ['-created']
    prepopulated_fields = {'slug': ('title_en',)}

# ----------------------------------
# Tag Admin
# ----------------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# ----------------------------------
# Subscriber Admin
# ----------------------------------
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    ordering = ['-subscribed_at']

# ----------------------------------
# Comment Admin
# ----------------------------------
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'approved', 'created')
    list_filter = ('approved', 'created')
    search_fields = ('name', 'email', 'content')

