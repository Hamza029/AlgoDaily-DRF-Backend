from datetime import datetime

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from authentication.models import User
from authentication.serializers import PostAuthorSerializer
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=300)
    author = PostAuthorSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    image = serializers.ImageField(required=False, read_only=False)
    # author_id = PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Blog
        # fields = '__all__'
        fields = ['id', 'title', 'description', 'created_at', 'image', 'author']

    def save(self, **kwargs):
        image = self.validated_data.get('image', None)
        if image is not None:
            # Generate a new file name using author id and timestamp
            ext = image.name.split('.')[-1]
            # create new image name
            new_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
            # Save the image with the new name
            image.name = new_filename
        return super().save(**kwargs)
