from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="群组名称")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wheel_groups")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "轮盘群组"
        verbose_name_plural = "轮盘群组s"

    def __str__(self):
        return self.name


class Option(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=100, verbose_name="选项内容")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "选项"
        verbose_name_plural = "选项s"

    def __str__(self):
        return f"{self.group.name} - {self.text}"
