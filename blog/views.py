from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Q

from blog.models import Blog


class BlogDetailView(DetailView):
    template_name = 'blog/detail.html'
    model = Blog
    context_object_name = 'blog'


class BlogView(ListView):
    template_name = 'blog/index.html'
    model = Blog
    paginate_by = 5
    context_object_name = 'blogs'


class BloggersView(ListView):
    template_name = 'blog/bloggers.html'
    context_object_name = 'bloggers'
    
    def get_queryset(self):
        permission = Permission.objects.get(codename='blogger')
        return get_user_model().objects.filter(
            Q(user_permissions=permission) | Q(is_superuser=True)).distinct()


class BloggerView(DetailView):
    template_name = 'blog/blogger.html'
    context_object_name = 'blogger'
    
    def get_queryset(self):
        permission = Permission.objects.get(codename='blogger')
        return get_user_model().objects.filter(
            Q(user_permissions=permission) | Q(is_superuser=True), pk=self.kwargs['pk'])
    
    
