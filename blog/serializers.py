from .models import Post, Comment, ReplyComment
from rest_framework import serializers
from bleach.css_sanitizer import CSSSanitizer
import bleach


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("author", "created_date", "updated_date", "published_date", "views")

    def validate_content(self, value):
        """
        make sure html content is safe by using bleach to sanitize it
        to avoid XSS attacks. Only allow a limited set of tags and attributes.
        """
        # allowed_tags = ['p', 'div', 'span', 'br', 'h1', 'h2', 'h3', 'code', 'pre', 'img', 'table', 'tr', 'td', 'th', 'a', 'strong', 'em']
        allowed_tags = [
            'p', 'div', 'span', 'br',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li',  # 新增：列表标签
            'blockquote', 'pre', 'code',  # 新增：引用和代码
            'hr',  # 新增：分割线
            'strong', 'em', 's', 'del', 'u',  # 新增：常见格式
            'img', 'a',
            'table', 'thead', 'tbody', 'tr', 'th', 'td',  # 表格
            'input'  # 新增：用于 Vditor 的任务列表复选框
        ]
        allowed_attrs = {
            '*': ['class', 'style','id', 'title'],   # 放宽：允许大部分标签使用 class（代码高亮需要）
            'a': ['href', 'target', 'rel', 'title'],
            'img': ['src', 'alt', 'title', 'width', 'height'],
            'input': ['type', 'checked', 'disabled'] # 任务列表支持
        }
        allowed_styles = ['color', 'font-weight', 'font-size', 'background-color', 'text-align', 'width', 'height']
        css_sanitizer = CSSSanitizer(allowed_css_properties=allowed_styles)
        return bleach.clean(value, tags=allowed_tags, attributes=allowed_attrs, css_sanitizer=css_sanitizer)
        # return bleach.clean(value)


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
