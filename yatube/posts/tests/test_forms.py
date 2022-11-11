from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.test_group = Group.objects.create(
            title='Тестовый заголовок',
            slug='slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост'
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create_form(self):
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост',
            'group': self.test_group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile',
                    kwargs={'username': self.user.username}),
        )
        self.assertEqual(Post.objects.count(),
                         posts_count + 1)

        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                group=self.test_group.id
            ).exists()
        )

    def test_post_edit_form(self):
        form_data = {
            'text': 'Измененный пост',
            'group': self.test_group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            user=self.user,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}),
        )
        self.post = Post.objects.get(id=self.post.id)

        self.assertEqual(self.post.text, form_data['text'])
