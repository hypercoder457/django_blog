"""Defines URL patterns for django_blogs."""

from typing import List

from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = 'django_blogs'

urlpatterns: List[URLPattern] = [
    # function views.
    path('', views.index, name="index"),  # Home page
    path('post/<int:post_id>/', views.post, name='post'),  # Post detail page.
    path('new_post/', views.new_post, name='new_post'),  # New post page
    path('new_comment/<int:post_id>/', views.new_comment,
         name='new_comment'),  # New comment page
    path('edit_post/<int:post_id>/', views.edit_post,
         name='edit_post'),  # Edit post page
    path('edit_comment/<int:comment_id>/',
         views.edit_comment, name='edit_comment'),  # Edit comment page.

    # Class based views.
    path('delete_post/<pk>/', views.PostDeleteView.as_view(),
         name='delete_post'),  # Very simple implementation
    # for deleting a post.
    path('delete_comment/<pk>/', views.CommentDeleteView.as_view(),
         name='delete_comment'),  # simple implementation
    # to delete a comment
    # The user profile page
    # Get access to the user's profile.
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('edit_profile/<username>/', views.edit_profile,
         name='edit_profile'),  # Edit a user's profile

    # View different users profiles.
    path('explore/', views.explore, name='explore'),
]
