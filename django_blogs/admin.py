from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Comment, CustomUser, Post


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['title', 'date_added']
    list_filter = ['date_added', 'title']


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Post, PostAdmin)
