import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.posts.models import Post, PostLike

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
class TestPostLike:

    def test_like_post(self, auth_client, post):
        """Можно лайкнуть пост"""
        url = reverse('post-like', kwargs={'slug': post.slug})
        response = auth_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        assert post.likes.count() == 1

    def test_unlike_post(self, auth_client, post, user):
        """Можно убрать лайк"""
        PostLike.objects.create(post=post, user=user)

        url = reverse('post-like', kwargs={'slug': post.slug})
        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert post.likes.count() == 0

    def test_double_like(self, auth_client, post, user):
        """Нельзя лайкнуть дважды"""
        PostLike.objects.create(post=post, user=user)

        url = reverse('post-like', kwargs={'slug': post.slug})
        response = auth_client.post(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_like_unauthenticated(self, client, post):
        """Неавторизованный пользователь не может лайкнуть"""
        url = reverse('post-like', kwargs={'slug': post.slug})
        response = client.post(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
