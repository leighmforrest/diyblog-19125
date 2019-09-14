from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client


class TestDataMixin:
    @classmethod
    def setUpTestData(cls):
        """Set up basic immutable data for the test."""
        # set up all users
        cls.user1 = get_user_model().objects.create_user(username='testuser1', password='12345', bio='x'*500)
        cls.user2 = get_user_model().objects.create_user(username='testuser2', password='12345', bio='z'*500)
        cls.commenter = get_user_model().objects.create_user(username='scrubby_mctroll', password='12345')

        # add permissions to users 1 and 2
        permission = Permission.objects.get(codename='blogger')
        cls.user1.user_permissions.add(permission)
        cls.user2.user_permissions.add(permission)

        # create basic blogs
        cls.blog = cls.user1.blogs.create(title='x'*128, description='z'*3000)
        cls.user1.blogs.create(title='y'*128, description='abc'*1000)
        cls.user1.blogs.create(title='d'*128, description='def'*1000)
        cls.user1.blogs.create(title='s'*128, description='ghi'*1000)

        # add comments
        cls.comment = cls.commenter.comments.create(blog=cls.blog, comment='d'*1024)
    
    def authenticated_client(self, username, password):
        """Helper to build authenticated client for tests."""
        client = Client()
        client.login(username=username, password=password)
        return client

