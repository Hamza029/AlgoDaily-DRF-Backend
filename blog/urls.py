from . import views
from django.urls import path


# --- for class based views ---


urlpatterns = [
    path("", views.BlogListAPIView.as_view(), name="post_list_create"),
    # path("<int:post_id>/", views.PostRetrieveUpdateDeleteView.as_view(), name="post_detail"),
]