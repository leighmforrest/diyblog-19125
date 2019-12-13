import random
import string

from django.test import TestCase
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse

from blog.tests.mixins import TestDataMixin
from blog.views import BloggersView


BLOGGER_PERMISSION = Permission.objects.get(codename='blogger')


def random_string(string_length=10):
    """Helper to generate dummy data"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


class TestBlogView(TestDataMixin, TestCase):
    def setUp(self):
        # make 3 test blogs
        for _ in range(3):
            self.user2.blogs.create(title=random_string(
                128), description=random_string(300))

        self.url = reverse('blog:index')
        self.response = self.client.get(self.url)

    def test_can_get_page(self):
        self.assertEqual(self.response.status_code, 200)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/index.html')

    def test_pagination_is_five(self):
        context = self.response.context
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['is_paginated'], True)
        self.assertTrue(len(context['blogs']), 5)

    def test_second_page(self):
        response = self.client.get('{}?page=2'.format(reverse('blog:index')))
        context = response.context
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['is_paginated'], True)
        self.assertTrue(len(context['blogs']), 2)


class TestBlogDetailView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:detail', args=[self.blog.pk])
        self.response = self.client.get(self.url)

    def test_can_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/detail.html')

    def test_context_is_blog(self):
        blog = self.response.context['blog']
        self.assertIsNotNone(blog)
        self.assertEqual(blog.title, self.blog.title)
        self.assertEqual(blog.description, self.blog.description)

    def test_comment_in_template(self):
        comment_h1 = '<h2>Comments</h2>'
        self.assertIn(comment_h1.encode('utf-8'), self.response.content)
        self.assertContains(self.response, '<div class="comments">', 1)
        self.assertContains(self.response, 'scrubby_mctroll', 1)


class TestBloggersView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:bloggers')
        self.response = self.client.get(self.url)

        # get the bloggers
        self.bloggers = get_user_model().objects.filter(
            Q(user_permissions=BLOGGER_PERMISSION) | Q(is_superuser=True)).distinct().order_by('username')

    def test_can_get(self):
        self.assertEqual(self.response.status_code, 200)

    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'blog/bloggers.html')

    def test_bloggers_in_context(self):
        bloggers = self.response.context['bloggers']
        for blogger in self.bloggers:
            self.assertTrue(blogger in bloggers)


class TestCommentCreateView(TestDataMixin, TestCase):
    def setUp(self):
        self.url = reverse('blog:create_comment', kwargs={'pk': self.blog.pk})
        self.data = {'comment': 'a'*512}

    def test_authenticated_user_can_get(self):
        client = self.authenticated_client(
            username=self.user1.username, password='12345')
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_post(self):
        client = self.authenticated_client(
            username=self.user1.username, password='12345')
        response = client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_redirect_after_post(self):
        client = self.authenticated_client(
            username=self.user1.username, password='12345')
        response = client.post(self.url, data=self.data)
        self.assertRedirects(response, reverse(
            'blog:detail', kwargs={'pk': self.blog.pk}))

    def test_anonymous_user_cannot_post(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_comment_in_comment_template(self):
        client = self.authenticated_client(
            username=self.user1.username, password='12345')
        response = client.post(self.url, data=self.data, follow=True)
        self.assertContains(response, self.data['comment'])
