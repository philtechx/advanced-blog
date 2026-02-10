from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('set-language/', include('blog.urls')),  # set-language stays outside i18n_patterns
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
)
