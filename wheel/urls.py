from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='wheel-group-list'),
    path('<int:group_id>/', views.group_detail, name='wheel-group-detail'),
    path('<int:group_id>/add-option/', views.add_option, name='wheel-add-option'),
    path('<int:group_id>/delete-option/<int:option_id>/', views.delete_option, name='wheel-delete-option'),
]
