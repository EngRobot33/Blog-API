from django.contrib.auth.models import User
from django.test import TestCase
from .models import Post


class PostTestCase(TestCase):
    def setUp(self):
        user_test = User.objects.create_user(username='admin2', password='hamed123')
        user_test.save()

        post_test = Post.objects.create(author=user_test, title='Title 2', content='Content 2')
        post_test.save()

    def test_blog(self):
        post = Post.objects.get(id=1)
        self.assertEqual(f'{post.author}', 'admin2')
        self.assertEqual(f'{post.title}', 'Title 2')
        self.assertEqual(f'{post.content}', 'Content 2')
