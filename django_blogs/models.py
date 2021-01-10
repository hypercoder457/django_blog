from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import ugettext as _
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
    username = models.CharField(
        _('Username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("That username is taken."),
        },
    )

    password = models.CharField(_('Password'), max_length=128)

    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=150,
        blank=True
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        unique=True,
        error_messages={
            'unique': _('That email is already taken.')
        },
        help_text=_('Required. Email addresses must be unique.')
    )

    bio = models.TextField(verbose_name=_('about me'), blank=True, null=True)

    avatar = ResizedImageField(size=[300, 300], upload_to='avatars')

    def __str__(self) -> str:
        return _(self.username)


class Post(models.Model):
    """A class that represents a single blog post."""
    title = models.CharField(verbose_name=_('post title'), max_length=200)
    body = models.TextField(verbose_name=_('post body'))
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return _(self.title)


class Comment(models.Model):
    """A class that represents a single comment.
    Comments are linked to posts."""
    comment_body = models.TextField(verbose_name=_('comment text'))
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{_(self.comment_body[:50])}..." if len(self.comment_body) > 50 else f"{_(self.comment_body[:50])}"
