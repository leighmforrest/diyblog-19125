from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.db.models import Q

from blog.models import Blog, Comment
from blog.forms import CommentForm


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
            Q(user_permissions=permission) | Q(is_superuser=True)).distinct().order_by('username')


class BloggerView(DetailView):
    template_name = 'blog/blogger.html'
    context_object_name = 'blogger'
    
    def get_queryset(self):
        permission = Permission.objects.get(codename='blogger')
        return get_user_model().objects.filter(
            Q(user_permissions=permission) | Q(is_superuser=True), pk=self.kwargs['pk'])


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'blog/create_comment.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = Blog.objects.get(pk=self.kwargs['pk'])
        return context
    
    def get_success_url(self):
        return Blog.objects.get(pk=self.kwargs['pk']).get_absolute_url()
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.blog = Blog.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
