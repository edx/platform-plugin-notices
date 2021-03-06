"""
Root API URLs.
All API URLs should be versioned, so urlpatterns should only
contain namespaces for the active versions of the API.
"""
from django.conf.urls import include, url


urlpatterns = [
    url(r"^v1/", include(("notices.rest_api.v1.urls", "v1"), namespace="v1")),
]
