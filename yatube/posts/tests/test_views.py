from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),

            'posts/group_list.html': (
                reverse('posts:group_list',
                        kwargs={'slug': PostPagesTests.group.slug})
            ),

            'posts/profile.html': (
                reverse('posts:profile',
                        kwargs={'username': PostPagesTests.user.username})
            ),

            'posts/create_post.html': reverse('posts:post_create'),

            'posts/post_detail.html': (
                reverse('posts:post_detail',
                        kwargs={'post_id': PostPagesTests.post.id})
            ),

            'posts/create_post.html': (
                reverse('posts:post_edit',
                        kwargs={'post_id': self.post.id})
            ),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def post_fields(self, post):
        with self.subTest(post=post):
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.author, self.post.author)
            self.assertEqual(post.group.id, self.post.group.id)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.post_fields(response.context['page_obj'][0])

    def test_groups_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.context['group'], self.group)
        self.post_fields(response.context['page_obj'][0])

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.user.username}))
        self.assertEqual(response.context['user'], self.user)
        self.post_fields(response.context['page_obj'][0])

    def test_detail_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}))
        self.post_fields(response.context['post'])


class PostPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='StasBasov')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='slug'
        )
        for i in range(13):
            cls.post = Post.objects.create(
                text='Тестовый пост',
                author=cls.user,
                group=cls.group
            )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index'),
            'posts:group_list': reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTests.group.slug}),
            'posts:profile': reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTests.user.username}),
        }
        for template, reverse_name in paginator_list.items():
            response = self.guest_client.get(reverse_name)
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_ten_posts(self):
        paginator_list = {
            'posts:index': reverse('posts:index') + '?page=2',
            'posts:group_list': reverse(
                'posts:group_list',
                kwargs={'slug': PostPaginatorTests.group.slug}) + '?page=2',
            'posts:profile': reverse(
                'posts:profile',
                kwargs={'username': PostPaginatorTests.user.username}
            ) + '?page=2',
        }
        for template, reverse_name in paginator_list.items():
            response = self.guest_client.get(reverse_name)
            self.assertEqual(len(response.context['page_obj']), 3)
