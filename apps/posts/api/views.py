from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from apps.posts.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer
from .permissions import IsOwnerOrReadOnly


class PostListView(generics.ListCreateAPIView):
    """
    GET - список постов (публичный)
    POST - создание поста (авторизованный)
    """
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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


