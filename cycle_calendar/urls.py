from django.urls import path
from . import views


urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),

    path('first/', views.first_visit, name='home'),

    path('follow/<int:followed_user>', views.CalendarFollowView.as_view(), name='calendar_follow'),
    path('follow/list', views.follow_list, name='follow_list'),
    path('follow/share/list', views.share_list, name='share_list'),
    path('follow/share/list/<int:pk>', views.delete_user_from_share_list, name='delete_user_from_share_list'),

    path('cycle-info/new/', views.cycle_info, name='cycle_info_new'),
    path('cycle-info/edit', views.update_cycle_info, name='cycle_edit'),

    path('cycle/new/', views.cycle_add_or_reset_date, name='cycle_new'),
    path('cycle/share', views.share_unique_text, name='cycle_share'),
    path('cycle/share/check', views.check_unique_text, name='cycle_check_share'),
]
