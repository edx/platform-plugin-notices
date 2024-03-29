"""
Root API URLs.
All API URLs should be versioned, so urlpatterns should only
contain namespaces for the active versions of the API.
"""
from django.urls import include, path


urlpatterns = [
    path("v1/", include(("notices.rest_api.v1.urls", "v1"), namespace="v1")),
]
