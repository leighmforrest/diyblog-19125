from django.urls import path, include

from blog.views import BlogView, BloggerView, BloggersView, BlogDetailView, CommentCreateView


app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name="index"),
    path('<uuid:pk>', BlogDetailView.as_view(), name="detail"),
    path('bloggers', BloggersView.as_view(), name="bloggers"),
    path('blogger/<uuid:pk>', BloggerView.as_view(), name="blogger"),
    path('<uuid:pk>/create', CommentCreateView.as_view(), name="create_comment"),
]