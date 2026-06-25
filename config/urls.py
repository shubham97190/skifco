from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'SKIFCO Foundation Admin'
admin.site.site_title = 'SKIFCO Admin'
admin.site.index_title = 'Dashboard'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('programs/', include('apps.programs.urls')),
    path('events/', include('apps.events.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('volunteer/', include('apps.volunteers.urls')),
    path('csr-partnerships/', include('apps.partnerships.urls')),
    path('reports/', include('apps.transparency.urls')),
    path('donate/', include('apps.donations.urls')),
    path('apply/', include('apps.beneficiaries.urls')),
    path('blog/', include('apps.news.urls')),
    path('account/', include('apps.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns = [
            path('__debug__/', include('debug_toolbar.urls')),
        ] + urlpatterns
