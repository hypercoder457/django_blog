from threading import Thread
from typing import Union

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMessage
from django.http import (Http404, HttpResponse, HttpResponsePermanentRedirect,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_blogs.forms import CustomUserCreationForm
from django_blogs.models import CustomUser

from .tokens import account_activation_token


def send_async_email(email: EmailMessage):
    email.send()


def register(request: WSGIRequest) -> HttpResponse:
    """Register a new user.
    This view has email confirmation."""
    if request.method != 'POST':
        form = CustomUserCreationForm()  # Display blank registration form.
    else:
        form = CustomUserCreationForm(data=request.POST)  # Process the form
        if form.is_valid():
            # The user won't be able to log in without email confirmation.
            # The line `new_user.is_active = False` does this.
            new_user: CustomUser = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            # Get the current site.
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'  # Email subject.

            # render a message with the `render_to_string` function and assign it to the variable message.
            message = render_to_string('registration/acc_active_email.html', {
                'user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user)
            })
            # Get the email address from the form.
            to_email = form.cleaned_data.get('email')

            # Make an instance of an `EmailMessage` object.
            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )

            # Send the email/return a response.
            Thread(target=send_async_email, args=(email,)).start()
            return render(request, 'registration/email_confirmation.html')

    # Display a blank/invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def activate(request: WSGIRequest, uidb64: bytes, token: str) -> Union[HttpResponseRedirect,
                                                                       HttpResponsePermanentRedirect, HttpResponse]:
    # error handling.
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))  # Decode the user id
        # Fetch the current user.
        current_user: CustomUser = get_object_or_404(CustomUser, pk=uid)
    except (TypeError, OverflowError, ValueError, Http404):
        current_user = None  # If an error occurs, the user most likely does not exist,
        # So set current_user to None.
    # Token check.
    if current_user is not None and account_activation_token.check_token(current_user, token):
        # Allow the user to log in. the line `current_user.is_active = True` does this.
        current_user.is_active = True
        current_user.save()  # Save the user.

        # Log the user in, and redirect back to the home page.
        # The user has been confirmed!!!!
        login(request, current_user)
        return redirect('django_blogs:index')
    else:
        # Invalid activation token, render a template saying the activation link was invalid.
        return render(request, 'registration/invalid_token.html')
