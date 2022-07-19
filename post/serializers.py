from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post


User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    def get_author(self, obj):
        return {
            "username": obj.author.username,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name,
            "email": obj.author.email,
        }

    author = serializers.SerializerMethodField('get_author')

    class Meta:
        model = Post
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',)