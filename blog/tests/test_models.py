from django.test import TestCase
from blog.tests.mixins import TestDataMixin
from django.urls import reverse

from blog.models import Blog, Comment


class BlogModelTest(TestDataMixin, TestCase):
    def test_blog_exists(self):
        blog = Blog.objects.first()
        self.assertIsNotNone(blog)
    
    def test_blog_fields(self):
        blog = self.blog
        self.assertEqual(blog.pk, self.blog.pk)
        self.assertEqual(blog.description, self.blog.description)
        self.assertEqual(blog.author, self.user1)
        self.assertIsNotNone(blog.created_at)
        self.assertIsNotNone(blog.updated_at)
    
    def test_create_blog(self):
        title='3'*128
        description='gdi'*1000
        blog = self.user1.blogs.create(title=title, description=description)
        self.assertIsNotNone(blog.pk)
        self.assertEqual(blog.title, title)
    
    def test_string(self):
        self.assertEqual(self.blog.title, str(self.blog))
    
    def test_get_absolute_url(self):
        url = reverse('blog:detail', kwargs={'pk': self.blog.pk})
        self.assertEqual(self.blog.get_absolute_url(), url)


class CommentModelTest(TestDataMixin, TestCase):
    def setUp(self):
        self.test_comment = self.blog.comments.create(author=self.commenter, comment='a'*1024)

    def test_comment_exists(self):
        self.assertIsNotNone(self.test_comment.comment)
    
    def test_create_comment(self):
        comment = self.blog.comments.create(author=self.commenter, comment='a'*1024)
        self.assertEqual(comment.blog.pk, self.blog.pk)
        self.assertEqual(comment.comment, 'a'*1024)
    
    def test_valid_fields(self):
        comment = Comment.objects.get(pk=self.test_comment.pk)
        self.assertEqual(self.test_comment, comment)
        self.assertEqual(comment.author, self.commenter)
    
    def test_long_string(self):
        content = 'Z'* 76
        self.test_comment.content = content
        self.assertEqual(self.test_comment.comment[:75] + '...', str(self.test_comment))
    
    def test_short_string(self):
        content = 'Z'* 15
        self.test_comment.comment = content
        self.assertEqual(self.test_comment.comment, str(self.test_comment))