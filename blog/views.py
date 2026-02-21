from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum
from django.contrib.auth import authenticate, login as d_login, logout as d_logout
from django.urls import reverse
from .models import Post, Category, Tag, Comment, ReplyComment
from pb.settings import BASE_DIR
from pathlib import Path
from wsgiref.util import FileWrapper
import mimetypes


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
    comments = Comment.objects.filter(post__id=post_id).order_by("-created_time")
    all_comments = { comment: ReplyComment.objects.filter(reply_to__id=comment.id) for comment in comments}
    comment_amount = 0
    comment_amount += len(all_comments.keys())
    for rc in all_comments.values():
        comment_amount += len(rc)
    post.increase_views()
    post_prev = Post.objects.filter(visible__name="public").filter(id__lt=post_id).order_by('-id').first()
    post_next = Post.objects.filter(visible__name="public").filter(id__gt=post_id).order_by('id').first()
    return render(request, "blog/blog_detail.html", {"post": post, "comments": all_comments, "comment_amount": comment_amount, "post_prev": post_prev, "post_next": post_next})


def blog_list(request):
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visible__name="public").order_by("published_date").reverse()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date").reverse()
    return pagination(request, posts)


def pagination(request, filter_posts):
    paginator = Paginator(filter_posts, 5)
    page = request.GET.get("page", 1)
    try:
        part_posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        part_posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of results
        part_posts = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_list.html", {"posts": filter_posts, "part_posts": part_posts})


def blog_list_sort(request, sort_type):
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visible__name="public").order_by('published_date').reverse()
    if login_user not in users:
        if sort_type == "date-desc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visible__name="public").order_by("published_date").reverse()
        elif sort_type == "date-asc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visible__name="public").order_by("published_date")
        elif sort_type == "views-desc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visible__name="public").order_by("views").reverse()
        elif sort_type == "views-asc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visible__name="public").order_by("views")
    else:
        if sort_type == "date-desc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date").reverse()
        elif sort_type == "date-asc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("published_date")
        elif sort_type == "views-desc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("views").reverse()
        elif sort_type == "views-asc":
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("views")
    return pagination(request, posts)


def archives(request):
    all_category = []
    all_tag = []
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        date_list = Post.objects.filter(visible__name="public").dates("published_date", "month", order="DESC")
        category_by_post_view = Category.objects.annotate(blog_views=Count("post__views")).filter(post__visible__name="public").order_by("-blog_views")
        tag_by_post_view = Tag.objects.annotate(blog_views=Sum("post__views")).filter(post__visible__name="public").order_by("-blog_views")
        for c in category_by_post_view:
            all_category.append(c.name)
        for t in tag_by_post_view:
            all_tag.append(t.name)
    else:
        date_list = Post.objects.dates("published_date", "month", order="DESC")
        category_by_post_view = Category.objects.annotate(blog_views=Count("post__views")).order_by("-blog_views")
        tag_by_post_view = Tag.objects.annotate(blog_views=Sum("post__views")).order_by("-blog_views")
        for c in category_by_post_view:
            all_category.append(c.name)
        for t in tag_by_post_view:
            all_tag.append(t.name)
    return render(request, "blog/category.html", context={"date_list": date_list, "category_list": all_category, "tag_list": all_tag})


def archives_date(request, year, month):
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        posts = Post.objects.filter(visible__name="public").filter(published_date__year=year, published_date__month=month).order_by("views").reverse()
    else:
        posts = Post.objects.filter(published_date__year=year, published_date__month=month).order_by("views").reverse()
    return pagination(request, posts)


def archives_category(request, category_name):
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        posts = Post.objects.filter(visible__name="public").filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by("views").reverse()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by("views").reverse()
    return pagination(request, posts)


def archives_tag(request, tag_name):
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        posts = Post.objects.filter(visible__name="public").filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by("views").reverse()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by("views").reverse()
    return pagination(request, posts)


def download_bak(request):
    if request.user.is_authenticated:
        bak_file = "other/db_bak/django_blog_v3-latest.sql"
        filename = Path(bak_file).name
        abs_path = Path(BASE_DIR).joinpath(bak_file)
        if abs_path.exists():
            chunk_size = 8192
            response = StreamingHttpResponse(FileWrapper(open(abs_path.as_posix(), "rb"), chunk_size), content_type=mimetypes.guess_type(abs_path)[0])
            response['Content-Length'] = abs_path.stat().st_size
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
        else:
            return HttpResponse('<h1>Cannot find the file</h1>')
    else:
        return render(request, "blog/error.html", {"error_type": "403"})


def update_comment_rate(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.increase_rate()
    return HttpResponse("comment rate increased")


def update_reply_rate(request, reply_id):
    reply = get_object_or_404(ReplyComment, pk=reply_id)
    reply.increase_rate()
    return HttpResponse("reply rate increased")


def do_login(request):
    if request.method == "POST":
        user_name = request.POST['user-name']
        user_pw = request.POST['user-pw']
        user = authenticate(username=user_name, password=user_pw)
        if user is not None:
            if user.is_active:
                d_login(request, user)
                return redirect(request.session["login_from"])  # go back to page before login
            else:
                request.session["login_error"] = "未激活用户"
                return render(request, "blog/login.html", {"username": user_name, "password": user_pw})
        else:
            request.session["login_error"] = "错误的用户名或密码"
            return render(request, 'blog/login.html', {"username": user_name, "password": user_pw})
    else: # such as GET
        request.session["login_from"] = request.META.get("HTTP_REFERER", "/")
        request.session["login_error"] = False
        user = request.user
        if user.is_authenticated:
            return redirect(reverse("blog-list"))
        else:
            return render(request, "blog/login.html")


def do_logout(request):
    d_logout(request)
    return redirect(reverse("index"))


def page_not_found(request, exception):
    return render(request, "blog/error.html", {"error_type": "404"})


def permission_denied(request, exception):
    return render(request, "blog/error.html", {"error_type": "403"})


def internal_error(request):
    return render(request, "blog/error.html", {"error_type": "500"})
