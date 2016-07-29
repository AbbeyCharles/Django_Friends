from django.conf.urls import url, patterns, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.accounts.urls')),
]
