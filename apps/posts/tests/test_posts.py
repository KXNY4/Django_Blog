import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpassword'
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def post(user):
    return Post.objects.create(
        author=user,
        title='Test Post',
        content='Test content',
        status=Post.Status.PUBLISHED
    )


@pytest.mark.django_db
class TestPostAPI:

    def test_list_posts_unauthenticated(self, client, post):
        """Список постов доступен без авторизации"""
        url = reverse('post-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_create_post_authenticated(self, auth_client):
        """Авторизованный пользователь может создать пост"""
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'New content',
            'status': 'published'
        }
        response = auth_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Post.objects.count() == 1

    def test_create_post_unauthenticated(self, client):
        """Неавторизованный не может создать пост"""
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'Content'
        }
        response = client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


    def test_update_own_post(self, auth_client, post):
        """Владелец может редактировать свой пост"""
        url = reverse('post-detail', kwargs={'slug': post.slug})
        response = auth_client.patch(url, {'title': 'Updated Title'})

        assert response.status_code == status.HTTP_200_OK
        post.refresh_from_db()
        assert post.title == 'Updated Title'

    def test_update_other_user_post(self, auth_client, user, db):
        """Нельзя редактировать чужой пост"""
        other_user = User.objects.create(
            email='other@example.com',
            username='other',
            password='otherpassword'
        )
        other_post = Post.objects.create(
            author=other_user,
            title='Other Post',
            content='Content',
            status=Post.Status.PUBLISHED
        )

        url = reverse('post-detail', kwargs={'slug': other_post.slug})
        response = auth_client.patch(url, {'title': 'Hacked'})

        assert response.status_code == status.HTTP_403_FORBIDDEN