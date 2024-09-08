from rest_framework import serializers

from authentication.serializers import PostAuthorSerializer
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=300)
    author = PostAuthorSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Blog
        # fields = '__all__'
        fields = ['id', 'title', 'description', 'created_at', 'author']
