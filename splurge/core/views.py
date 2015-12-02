from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login, authenticate
from django.http.request import QueryDict
from .models import AppUser, Employee, Team, GiftCard, GiftCardCategory
from .tasks import activation_mail_queue


def home(request):
    if request.user.is_anonymous():
        return redirect('homepage')
    else:
        return render_to_response("home.html", RequestContext(request))


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


@login_required
def teams(request):
    team = request.user.teams.all()
    return render_to_response("teams.html", RequestContext(request, {
        "teams": team
    }))


@login_required
def employees(request):
    employee = request.user.employees.all()
    return render_to_response("employees.html", RequestContext(request, {
        "employees": employee
    }))


@login_required
def create_team(request):
    if request.method == 'GET':
        employees = request.user.employees.all()
        return render_to_response("add_team.html", RequestContext(request, {
            "employees": employees
        }))
    else:
        employees = request.POST.getlist("employees")
        team_name = request.POST.get("teamName")
        t = Team(
            name=team_name,
            app_user=request.user
        )
        t.save()
        for e in employees:
            emp_object = Employee.objects.get(pk=int(e))
            emp_object.team = t
            emp_object.save()
        return redirect('teams')


@login_required
def add_employee(request):
    if request.method == 'GET':
        return render_to_response("add_employee.html", RequestContext(request, {

        }))
    else:
        e = Employee(
            first_name=request.POST.get("firstName"),
            last_name=request.POST.get("lastName"),
            email_id=request.POST.get("emailID"),
            phone_number=request.POST.get("phoneNumber"),
            app_user=request.user
        )
        e.save()
        return redirect('employees')


@login_required
def delete_employee(request, employee_id):
    employee_id = int(employee_id)
    e = Employee.objects.get(pk=employee_id)
    e.delete()
    return redirect('employees')


@login_required
def cards(request):
    gift_cards = request.user.gift_cards.all()
    return render_to_response("gift_card.html", RequestContext(request, {
        "gift_cards": gift_cards
    }))


@login_required
def send_card_to_employee(request):
    if request.method == 'GET':
        employees = request.user.employees.all()
        categories = GiftCardCategory.objects.all()
        return render_to_response("add_card_to_employee.html", RequestContext(request, {
            "employees": employees,
            "categories": categories
        }))
    else:
        employee = request.POST.get("employees")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        category_obj = GiftCardCategory.objects.get(pk=int(category))
        gc = GiftCard(
            amount=amount,
            to=Employee.objects.get(pk=(int(employee))),
            given_by=request.user,
            category=category_obj
        )
        gc.save()
        return redirect('cards')


@login_required
def send_card_to_a_team(request):
    if request.method == 'GET':
        teams = request.user.teams.all()
        categories = GiftCardCategory.objects.all()
        return render_to_response("add_card_to_team.html", RequestContext(request, {
            "teams": teams,
            "categories": categories
        }))
    else:
        team = request.POST.get("teams")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        category_obj = GiftCardCategory.objects.get(pk=int(category))
        team_obj = Team.objects.get(pk=int(team))
        for u in team_obj.employees.all():
            gc = GiftCard(
                amount=amount,
                to=u,
                given_by=request.user,
                category=category_obj
            )
            gc.save()
        return redirect('cards')


@login_required
def create_card_for_employee(request, employee_id):
    employee_obj = Employee.objects.get(pk=int(employee_id))
    categories = GiftCardCategory.objects.all()
    if request.method == 'GET':
        return render_to_response("card_to_specific_employee.html", RequestContext(request, {
            "employee": employee_obj,
            "categories": categories
        }))
    else:
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        category_obj = GiftCardCategory.objects.get(pk=int(category))
        gc = GiftCard(
            amount=amount,
            to=employee_obj,
            given_by=request.user,
            category=category_obj
        )
        gc.save()
        return redirect('cards')


@login_required
def create_card_for_team(request, team_id):
    team_obj = Team.objects.get(pk=int(team_id))
    categories = GiftCardCategory.objects.all()
    if request.method == 'GET':
        return render_to_response("card_to_specific_team.html", RequestContext(request, {
            "team": team_obj,
            "categories": categories
        }))
    else:
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        category_obj = GiftCardCategory.objects.get(pk=int(category))
        for e in team_obj.employees.all():
            gc = GiftCard(
                amount=amount,
                to=e,
                given_by=request.user,
                category=category_obj
            )
            gc.save()
        return redirect('cards')
