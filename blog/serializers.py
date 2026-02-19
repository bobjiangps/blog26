from .models import Post, Comment, ReplyComment
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("rate",)


class ReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplyComment
        fields = "__all__"

class ReplyUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplyComment
        fields = ("rate",)
