from .models import Post, Comment, ReplyComment
from .serializers import PostSerializer, CommentSerializer, ReplySerializer, CommentUpdateSerializer, ReplyUpdateSerializer
from django.db.models import Q
from django.utils import timezone

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    # queryset = Post.objects.filter(visible__name="public").order_by("-published_date")
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(Q(visible__name="public") | Q(author=self.request.user.id)).order_by("-published_date")
        return queryset

    def perform_create(self, serializer):
        # 创建时手动注入作者，且不设置 updated_date
        serializer.save(author=self.request.user, published_date=timezone.now())

    def perform_update(self, serializer):
        # 更新时自动设置当前时间为更新时间
        serializer.save(updated_date=timezone.now())

    def update(self, request, *args, **kwargs):
        # 只允许作者本人修改自己的文章
        instance = self.get_object()
        if instance.author != request.user:
            return Response(
                {"detail": "Not allowed to edit others' posts"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return Response({"message": "delete action is not allowed, contact administrator"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# class CommentViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.ListModelMixin,
#                   viewsets.GenericViewSet):
#
#     queryset = Comment.objects.order_by("-created_time")
#     serializer_class = CommentSerializer


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.order_by("-created_time")
    serializer_class = CommentSerializer


class CommentUpdate(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.order_by("-created_time")
    serializer_class = CommentSerializer

    def put(self, request, *args, **kwargs):
        current_comment = Comment.objects.filter(id=kwargs["pk"])
        request.data._mutable = True
        request.data["rate"] = current_comment[0].rate + 1
        self.serializer_class = CommentUpdateSerializer
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        current_comment = Comment.objects.filter(id=kwargs["pk"])
        request.data._mutable = True
        request.data["rate"] = current_comment[0].rate + 1
        self.serializer_class = CommentUpdateSerializer
        return self.partial_update(request, *args, **kwargs)


# class ReplyViewSet(mixins.CreateModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.ListModelMixin,
#                   viewsets.GenericViewSet):
#
#     queryset = ReplyComment.objects.order_by("-created_time")
#     serializer_class = ReplySerializer


class ReplyList(generics.ListCreateAPIView):
    queryset = ReplyComment.objects.order_by("-created_time")
    serializer_class = ReplySerializer


class ReplyUpdate(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.order_by("-created_time")
    serializer_class = ReplySerializer

    def put(self, request, *args, **kwargs):
        current_reply = ReplyComment.objects.filter(id=kwargs["pk"])
        request.data._mutable = True
        request.data["rate"] = current_reply[0].rate + 1
        self.serializer_class = ReplyUpdateSerializer
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        current_reply = ReplyComment.objects.filter(id=kwargs["pk"])
        request.data._mutable = True
        request.data["rate"] = current_reply[0].rate + 1
        self.serializer_class = ReplyUpdateSerializer
        return self.partial_update(request, *args, **kwargs)
