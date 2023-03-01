from django.urls import path
from . import views


urlpatterns = [
    path('', views.forum_post_list, name='forum_post_list'),
    path('post/<int:pk>/', views.forum_post_detail, name='forum_post_detail'),
    path('category/<str:name>/', views.forum_category_detail, name='forum_category_detail'),
    path('new/', views.new_post, name='new_post'),
    path('new/done/', views.done_post, name='done_post'),
]
