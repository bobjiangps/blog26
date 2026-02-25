from django.urls import path, re_path
from . import views, views_api


urlpatterns = [
    path('', views.index_articles, name='index'),
    path('blog-list/', views.blog_list, name='blog-list'),
    path('article-01<int:post_id>/', views.blog_detail, name='blog-detail'),
    path('article-01<int:post_id>/edit', views.blog_edit, name='blog-edit'),
    path('create-new/', views.create_new, name='create-new'),
    path('download_bak/', views.download_bak, name='download-bak'),
    path('update-comment-rate-<int:comment_id>/', views.update_comment_rate, name='update-comment-rate'),
    path('update-reply-rate-<int:reply_id>/', views.update_reply_rate, name='update-reply-rate'),
    path('blog-list/sort-by-<str:sort_type>/', views.blog_list_sort, name='blog-list-sort'),
    path('categorization/', views.archives, name='archives'),
    path('categorization/<int:year>/<int:month>/', views.archives_date, name='archives-date'),
    path('categorization/category/<str:category_name>/', views.archives_category, name='archives-category'),
    path('categorization/tag/<str:tag_name>/', views.archives_tag, name='archives-tag'),
    path('login/', views.do_login, name='do-login'),
    path('logout/', views.do_logout, name='do-logout'),
    path('api/posts/', views_api.PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='posts-api'),
    re_path('api/posts/(?P<pk>[0-9]+)/', views_api.PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update'}), name='post-detail-api'),
    path('api/comments/', views_api.CommentList.as_view(), name='comments-api'),
    # re_path('api/comments/(?P<pk>[0-9]+)/', views_api.CommentUpdate.as_view(), name='comment-detail-api'),
    path('api/replies/', views_api.ReplyList.as_view(), name='replies-api'),
    # re_path('api/replies/(?P<pk>[0-9]+)/', views_api.ReplyUpdate.as_view(), name='reply-detail-api'),
    path('api/vditor/upload/', views.vditor_upload, name='vditor-upload'),
]
