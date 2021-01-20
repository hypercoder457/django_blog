from typing import Any, Dict, Optional, Union

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Model
from django.db.models.manager import BaseManager
from django.http import (Http404, HttpResponse, HttpResponsePermanentRedirect,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import DeleteView

from .forms import CommentForm, EditProfileForm, PostForm
from .models import Comment, CustomUser, Post


def check_post_owner(request: WSGIRequest, post: Post) -> None:
    """Helper function to check
    that the post owner is the 'actual' owner of the post."""
    if post.owner != request.user:
        raise Http404


def index(request: WSGIRequest) -> HttpResponse:
    """The home page for this Django blog.
    This shows all posts as well, with the post title acting as a link to
    a detail page."""
    posts: BaseManager = Post.objects.order_by('date_added')
    context: Dict[str, BaseManager[Model]] = {'posts': posts}
    return render(request, 'django_blogs/index.html', context)


def post(request: WSGIRequest, post_id: int) -> HttpResponse:
    """Show a single post & all of the associated comments."""
    post = get_object_or_404(Post, id=post_id)
    comments: Any = post.comment_set.all()
    context = {'post': post, 'comments': comments}
    return render(request, 'django_blogs/post.html', context)


@login_required
def new_post(request: WSGIRequest) -> Union[HttpResponseRedirect,
                                            HttpResponsePermanentRedirect, HttpResponse]:
    """Create a new post."""
    if request.method != 'POST':
        form = PostForm()  # Display blank post creation form.
    else:
        # If the form is submitted, process the data. This is a POST request.
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post: Post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('django_blogs:index')
    # Display a blank/invalid form.
    context = {'form': form}
    return render(request, 'django_blogs/new_post.html', context)


@login_required
def new_comment(request: WSGIRequest, post_id: int) -> Union[HttpResponseRedirect,
                                                             HttpResponsePermanentRedirect, HttpResponse]:
    """Add a new comment, associated with a post."""
    post = get_object_or_404(Post, id=post_id)
    check_post_owner(request, post)
    if request.method != 'POST':
        form = CommentForm()  # Display blank comment form.
    else:
        # Process the comment form with data=request.POST
        form = CommentForm(data=request.POST)
        if form.is_valid():
            if post.owner == request.user:
                comment: Comment = form.save(commit=False)
                comment.post = post
                comment.save()
            return redirect('django_blogs:post', post_id=post_id)
    # Display a blank/invalid form.
    context = {'post': post, 'form': form}
    return render(request, 'django_blogs/new_comment.html', context)


@login_required
def edit_post(request: WSGIRequest, post_id: int) -> Union[HttpResponseRedirect,
                                                           HttpResponsePermanentRedirect, HttpResponse]:
    """Edit a post."""
    post = get_object_or_404(Post, id=post_id)
    check_post_owner(request, post)
    if request.method != 'POST':
        # Pre-fill form with the current post.
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)  # Process the data.
        if form.is_valid():
            form.save()
            return redirect('django_blogs:index')
    # Display blank/invalid form.
    context = {'post': post, 'form': form}
    return render(request, 'django_blogs/edit_post.html', context)


@login_required
def edit_comment(request: WSGIRequest, comment_id: int) -> Union[HttpResponseRedirect,
                                                                 HttpResponsePermanentRedirect, HttpResponse]:
    """Edit a comment."""
    comment: Comment = get_object_or_404(Comment, id=comment_id)
    post: Post = comment.post
    if request.method != 'POST':
        form = CommentForm(instance=comment)  # Pre-fill comment form
    else:
        # Process the data from the form.
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('django_blogs:post', post_id=post.id)

    # Display a blank/invalid form.
    context = {'comment': comment, 'post': post, 'form': form}
    return render(request, 'django_blogs/edit_comment.html', context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """This is a CLASS BASED VIEW. This is simple, as it allows users to delete posts."""
    model = Post
    success_url = "/"
    template_name = 'django_blogs/post_delete.html'

    def test_func(self) -> Optional[bool]:
        return self.get_object().owner == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Another class based view, allowing users to delete comments
    that are associated with posts."""
    model = Comment
    success_url = "/"
    template_name = 'django_blogs/comment_delete.html'

    def test_func(self) -> Optional[bool]:
        return self.get_object().post.owner == self.request.user


@login_required
def user_profile(request: WSGIRequest, username: str) -> HttpResponse:
    """View a user profile."""
    user: CustomUser = get_object_or_404(CustomUser, username=username)
    posts: BaseManager = Post.objects.filter(owner=user)
    context = {'user': user, 'posts': posts, 'request': request}
    return render(request, 'django_blogs/user_profile.html', context)


@login_required
def edit_profile(request: WSGIRequest, username: str) -> Union[HttpResponseRedirect,
                                                               HttpResponsePermanentRedirect, HttpResponse]:
    """Edit a user's profile."""
    user: CustomUser = get_object_or_404(CustomUser, username=username)
    if request.method != 'POST':
        form = EditProfileForm(instance=user)
    else:
        form = EditProfileForm(
            instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('django_blogs:user_profile', username=user.username)

    context = {'form': form, 'user': user}
    return render(request, 'django_blogs/edit_profile.html', context)


@login_required
def explore(request: WSGIRequest) -> HttpResponse:
    """The explore page.
    Allows users to view other user's profiles
    by direct access from this page."""
    users: BaseManager = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'django_blogs/explore.html', context)
