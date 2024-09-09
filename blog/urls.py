from . import views
from django.urls import path


# --- for class based views ---


urlpatterns = [
    path("", views.BlogListAPIView.as_view(), name="blog_list_create"),
    path("<uuid:blog_id>/", views.BlogRetrieveUpdateDestroyView.as_view(), name="post_detail"),
]