<<<<<<< HEAD
"""
URL configuration for myblog project.

Handles:
- Admin routes
- Blog routes
- Language switching (English / Swahili)
- Media serving in development
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


# ==========================
# MAIN URL PATTERNS
# ==========================

urlpatterns = [
    # Language switcher route (for changing EN/SW)
    path('i18n/', include('django.conf.urls.i18n')),
]


# ==========================
# LANGUAGE-AWARE ROUTES
# ==========================
# These URLs will automatically become:
# /en/...
# /sw/...

urlpatterns += i18n_patterns(
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Blog App URLs
    path('', include('blog.urls')),
)


# ==========================
# MEDIA FILES (DEV ONLY)
# ==========================

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
=======
"""
URL configuration for myblog project.

Handles:
- Admin routes
- Blog routes
- Language switching (English / Swahili)
- Media serving in development
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


# ==========================
# MAIN URL PATTERNS
# ==========================

urlpatterns = [
    # Language switcher route (for changing EN/SW)
    path('i18n/', include('django.conf.urls.i18n')),
]


# ==========================
# LANGUAGE-AWARE ROUTES
# ==========================
# These URLs will automatically become:
# /en/...
# /sw/...

urlpatterns += i18n_patterns(
    # Django Admin Panel
    path('admin/', admin.site.urls),

    # Blog App URLs
    path('', include('blog.urls')),
)


# ==========================
# MEDIA FILES (DEV ONLY)
# ==========================

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 4a481a0 (Updated blog added comment system and authentication)
