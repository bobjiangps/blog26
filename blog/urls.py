from django.urls import path, re_path
from . import views, views_api


urlpatterns = [
    path('', views.index_articles, name="index"),
    path('article-01<int:post_id>/', views.blog_detail, name="blog-detail"),
    path('download_bak/', views.download_bak, name='download-bak'),
    # path('error', views.show_error, name="error"),
    # path('login', views.index_articles, name="login"),
    path('api/posts/', views_api.PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts-api'),
    re_path('api/posts/(?P<pk>[0-9]+)/', views_api.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='post-detail-api'),
    path('api/comments/', views_api.CommentList.as_view(), name='comments-api'),
    re_path('api/comments/(?P<pk>[0-9]+)/', views_api.CommentUpdate.as_view(), name='comment-detail-api'),
    path('api/replies/', views_api.ReplyList.as_view(), name='replies-api'),
    re_path('api/replies/(?P<pk>[0-9]+)/', views_api.ReplyUpdate.as_view(), name='reply-detail-api'),
]
