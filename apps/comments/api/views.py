from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.comments.models import Comment
from apps.posts.api.permissions import IsOwnerOrReadOnly
from apps.posts.models import Post

from .serializers import CommentSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Comment.objects.filter(post__slug=slug)
    
    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug)
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'









