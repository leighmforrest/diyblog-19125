from django.contrib import admin

from blog.models import Blog, Comment


class CommentInline(admin.TabularInline):
    model = Comment

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [CommentInline,]

admin.site.register(Blog, BlogAdmin)
