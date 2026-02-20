from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Visible(models.Model):
    visible_options = (("0", "public"),("1", "private"))
    name = models.CharField(max_length=50, choices=visible_options, default=visible_options[0])

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)
    summary = models.CharField(max_length=1000, blank=True, null=True)
    img_url = models.URLField(max_length=200, blank=True, null=True)
    content = RichTextUploadingField()
    visible = models.ForeignKey(Visible, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def update(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        # update_fields 只更新数据库中的views
        self.save(update_fields=["views"])


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.content[:20]

    def increase_rate(self):
        self.rate += 1
        self.save(update_fields=["rate"])

class ReplyComment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    reply_to = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_to_name = models.CharField(max_length=100, default="unknown")
    rate = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.content[:20]

    def increase_rate(self):
        self.rate += 1
        self.save(update_fields=["rate"])
