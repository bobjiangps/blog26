from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag, Comment, ReplyComment


def index_articles(request):
    amount = 5
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        new_posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visible__name="public").order_by("-published_date")
    else:
        new_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("-published_date")
    # for the posts which set to top
    top_posts = Post.objects.filter(id__in=[104, 255, 180, 263, 282]).order_by("views").reverse()
    extra_info = { "article_amount": Post.objects.count(), "category_amount": Category.objects.count()}
    return render(request, "blog/index.html", {"top_posts": top_posts[:amount], "new_posts": new_posts[:amount], "info": extra_info})


def blog_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.visible.name == "private" and request.user.is_authenticated is False:
        return render(request, "blog/error.html", {"error_type": "403"})
    comments = Comment.objects.filter(post__id=post_id)
    all_comments = { comment: ReplyComment.objects.filter(reply_to__id=comment.id) for comment in comments}
    post.increase_views()
    post_prev = Post.objects.filter(visible__name="public").filter(id__lt=post_id).order_by('-id').first()
    post_next = Post.objects.filter(visible__name="public").filter(id__gt=post_id).order_by('id').first()
    return render(request, "blog/blog_detail.html", {"post": post, "comments": all_comments, "post_prev": post_prev, "post_next": post_next})
