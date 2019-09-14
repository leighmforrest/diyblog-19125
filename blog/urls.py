from django.urls import path, include

from blog.views import BlogView, BloggerView, BloggersView, BlogDetailView


app_name = 'blog'

urlpatterns = [
    path('', BlogView.as_view(), name="index"),
    path('<uuid:pk>', BlogDetailView.as_view(), name="detail"),
    path('bloggers', BloggersView.as_view(), name="bloggers"),
    path('blogger/<uuid:pk>', BloggerView.as_view(), name="blogger"),
]