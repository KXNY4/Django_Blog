import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuth:

    def test_register(self, client):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password_confirm': 'testpassword',
        }
        response = client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=data['email']).exists()

    def test_register_password_mismatch(self, client):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password_confirm': 'difftestpassword'
        }
        response = client.post(url, email=data['email'], password=data['password'])

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login(self, client, db):
        User.objects.create_user(
            email = 'test@example.com',
            username = 'testuser',
            password = 'testpassword'
        )
        url = reverse('token_obtain_pair')
        response = client.post(url, {'email': 'test@example.com', 'password': 'testpassword'})

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data




