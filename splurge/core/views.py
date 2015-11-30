from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login, authenticate

from .models import AppUser
from .tasks import activation_mail_queue


def home(request):
    if request.user.is_anonymous():
        context_instance = RequestContext(request, {})
        return render_to_response("home.html", context_instance)


def signup(request):
    context_instance = RequestContext(request, {})
    if request.method == 'GET':
        return render_to_response("signup.html", context_instance)
    else:
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        email = request.POST.get("email")
        organisation = request.POST.get("organisation")
        password = request.POST.get("password")
        appuser = AppUser(
            first_name=first_name,
            last_name=last_name,
            organisation_name=organisation,
            email=email,
            username=email,
            is_active=False
        )
        appuser.save()
        appuser.set_password(password)
        appuser.save()
        activation_mail_queue.delay(appuser)
        return render_to_response("home.html", RequestContext(request, {'success': True}))


def login(request):
    context_instance = RequestContext(request, {})
    if request.method == 'GET':
        return render_to_response("login.html", context_instance)
    else:
        username = request.POST.get("userName")
        password = request.POST.get("password")
        appuser = authenticate(username=username, password=password)
        if appuser is not None:
            if appuser.is_active:
                auth_login(request, appuser)
                return redirect('homepage')
            else:
                return render_to_response("login.html", RequestContext(request, {
                    "errors": True,
                    "error": "Please activate your account by clicking on the link."
                }))
        return render_to_response("login.html", RequestContext(request, {
            "errors": True,
            "error": "Invalid Credentials!"
        }))


@login_required
def homepage(request):
    print request.user
    context_instance = RequestContext(request)
    return render_to_response("homepage.html", context_instance)


def activate_user(request, unique_id):
    try:
        user = AppUser.objects.get(unique_code=unique_id)
        user.is_active = True
        user.save()
        return render_to_response("login.html", RequestContext(request, {
            "success": True,
            "message": "Account activated login to continue!"
        }))
    except ObjectDoesNotExist:
        return render_to_response("error.html", RequestContext(request))
