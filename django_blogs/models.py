from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField


class CustomUser(AbstractUser):
    """
    This model is a subclass of the `AbstractUser` model.
    It overrides the model field `email` to set unique to True
    so that people MUST enter their email when they register in the app.
    unique also enables a checker that will not proceed if there is an email in the database
    and the user enters that SAME email on a registration form.
    The error messages property
    enables custom error messages!
    """
    email = models.EmailField(
        'Email address',
        unique=True,
        error_messages={
            'unique': 'A user with that email address already exists.'
        },
        help_text='Required. Email addresses must be unique.'
    )

    bio = models.TextField('about me', blank=True, null=True)

    avatar = ResizedImageField(size=[300, 300], upload_to='avatars')

    def __str__(self) -> str:
        return self.username


class Post(models.Model):
    """A class that represents a single blog post."""
    title = models.CharField('post title', max_length=200)
    body = models.TextField('post body')
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """A class that represents a single comment.
    Comments are linked to posts."""
    comment_body = models.TextField('comment text')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.comment_body[:50]}..." if len(self.comment_body) > 50 else f"{self.comment_body[:50]}"
