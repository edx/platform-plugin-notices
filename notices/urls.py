"""
URLs for notices.
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r"", include(("notices.rest_api.urls", "rest_api"), namespace="rest_api"))
]
