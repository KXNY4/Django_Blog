from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.posts.models import Post, Tag


User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar'] 

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'excerpt', 'content', 'author', 'image', 'category', 'tags', 'created_at']

    def get_excerpt(self, obj):
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content
    

class PostDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'author', 'image', 'category', 'tags', 'status', 'created_at', 'updated_at']


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'status', 'category', 'tags']