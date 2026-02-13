from django.contrib import admin

from apps.posts.models import Category, Post, PostLike, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    read_only_fields = ('slug', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    read_only_fields = ('slug', 'created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(PostLike)
