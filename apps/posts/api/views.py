from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter  
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.posts.models import Category, Post, PostLike, Tag
from .serializers import CategorySerializer, PostListSerializer, PostDetailSerializer, PostCreateSerializer, TagSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import PostFilter


class PostListView(generics.ListCreateAPIView):
    """
    GET - список постов (публичный)
    POST - создание поста (авторизованный)
    """
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter] 
    filterset_class = PostFilter
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET - детали поста
    PATCH - редактирование (только автор)
    DELETE - удаление (только  автор)
    """
    queryset = Post.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateSerializer
        return PostDetailSerializer


class MyPostsView(generics.ListAPIView):
    """Мои посты (включая черновики)"""
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug):
        """Лайк поста"""
        post = get_object_or_404(Post, slug=slug)
        like, created = PostLike.objects.get_or_create(post=post, user=request.user)

        if not created:
            return Response(
                {"detail": "Вы уже лайкнули этот пост"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"detail": "Лайк добавлен"}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, slug):
        """Удаление лайка"""
        post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
        deleted, _ = PostLike.objects.filter(post=post, user=request.user).delete()

        if not deleted:
            return Response(
                {"detail": "Вы не лайкали этот пост"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"detail": "Лайк удалён"}, status=status.HTTP_204_NO_CONTENT)


class CategoryListView(generics.ListAPIView):
    """Список категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    """Детали категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class TagListView(generics.ListAPIView):
    """Список тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class TagDetailView(generics.RetrieveAPIView):
    """Список тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


