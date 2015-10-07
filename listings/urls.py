from django.conf.urls import include, url
from listings.views import get_listings

urlpatterns = [
    url(r'^$', get_listings),
]
