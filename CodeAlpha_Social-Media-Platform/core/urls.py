from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('explore/', views.explore_view, name='explore'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('api/notifications/unread/', views.notifications_unread, name='notifications_unread'),
    path('api/notifications/mark-read/', views.mark_notifications_read, name='mark_notifications_read'),

    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('settings/profile/', views.edit_profile, name='edit_profile'),
]
