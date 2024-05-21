from rest_framework import serializers
from blog.models import BlogPost
from accounts.models import HomePhoto


class HomePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePhoto
        fields = ('image', 'photo_type')

class BlogPostSerializer(serializers.ModelSerializer):
    user_photos = HomePhotoSerializer(many=True, read_only=True, source='user.home_photos')

    class Meta:
        model = BlogPost
        fields = '__all__'