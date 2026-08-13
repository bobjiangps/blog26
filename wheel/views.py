from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Group, Option


def group_list(request):
    """群组列表页：只有登录用户可访问和创建"""
    if not request.user.is_authenticated:
        return render(request, "blog/error.html", {"error_type": "403"}, status=403)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            Group.objects.create(name=name, created_by=request.user)
        return redirect("wheel-group-list")

    groups = Group.objects.all()
    return render(request, "wheel/group_list.html", {"groups": groups})


def group_detail(request, group_id):
    """群组详情页：所有人可访问"""
    group = get_object_or_404(Group, pk=group_id)
    options = list(group.options.values("id", "text"))
    return render(request, "wheel/group_detail.html", {
        "group": group,
        "options": options,
        "options_json": json.dumps(options, ensure_ascii=False),
    })


@csrf_exempt
def add_option(request, group_id):
    """添加选项：游客也可以添加，无需 CSRF（公开无敏感操作）"""
    group = get_object_or_404(Group, pk=group_id)
    try:
        data = json.loads(request.body)
        text = data.get("text", "").strip()
    except (json.JSONDecodeError, AttributeError):
        text = request.POST.get("text", "").strip()

    if not text:
        return JsonResponse({"error": "选项内容不能为空"}, status=400)

    option = Option.objects.create(group=group, text=text)
    options = list(group.options.values("id", "text"))
    return JsonResponse({"id": option.id, "text": option.text, "options": options})


@login_required
@require_POST
def delete_option(request, group_id, option_id):
    group = get_object_or_404(Group, pk=group_id)
    option = get_object_or_404(Option, pk=option_id, group=group)
    option.delete()
    options = list(group.options.values("id", "text"))
    return JsonResponse({"success": True, "options": options})
