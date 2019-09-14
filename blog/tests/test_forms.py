from django.test import TestCase

from blog.tests.mixins import TestDataMixin
from blog.forms import CommentForm


class TestCommentForm(TestDataMixin, TestCase):
    def test_valid_comment(self):
        data = {'comment': 'Z' * 1024}
        form = CommentForm(data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_comment(self):
        data = {'comment': 'z' * 1025}
        form = CommentForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'comment': ['The comment is too long.']})
    
    def test_blank_comment(self):
        form = CommentForm({'comment': ''})
        self.assertEqual(form.errors, {'comment': ['This field is required.']})
    
    def test_comment_label(self):
        form = CommentForm()
        self.assertTrue(form.fields['comment'].label == 'Description')