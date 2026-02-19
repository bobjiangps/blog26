from django.urls import path
from . import views


urlpatterns = [
    path('', views.index_articles, name="index"),
    path('article-01<int:post_id>/', views.blog_detail, name="blog-detail"),
    path('download_bak/', views.download_bak, name='download-bak')
    # path('error', views.show_error, name="error"),
    # path('login', views.index_articles, name="login"),
]
