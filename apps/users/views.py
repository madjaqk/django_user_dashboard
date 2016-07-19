from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import RegisterForm, LoginForm
from .utils import require_login

def login_page(request):
	context = {"reg_form": RegisterForm(), "login_form": LoginForm()}
	return render(request, "users/login.html", context)

def login(request):
	curr_user = User.user_manager.login(request.POST["email_address"], request.POST["password"])
	if not curr_user:
		messages.error(request, "E-mail or password incorrect")
		return redirect("login_page")
	else:
		request.session["curr_user"] = curr_user.id
		return redirect("dashboard")

def register(request):
	registered, guy_or_errors = User.user_manager.register(request.POST)
	
	if not registered:
		for error in guy_or_errors: messages.error(request, error)
		return redirect("login_page")
	else:
		request.session["curr_user"] = guy_or_errors.id
		return redirect("dashboard")
	

def log_off(request):
	request.session.clear()
	return redirect("login_page")

@require_login
def dashboard(request, curr_user):
	context = {
		"curr_user": curr_user,
		"users": User.user_manager.all(),
	}
	return render(request, "users/dashboard.html", context)

@require_login
def show(request, curr_user, id):
	print("show page")
	context = {
		"curr_user": curr_user,
		"user": User.user_manager.get(id=id),
	}

	return render(request, "users/show.html", context)

@require_login
def edit(request, curr_user, id):
	context = {
		"curr_user": curr_user,
		"user": User.user_manager.get(id=id),
	}
	return render(request, "users/edit.html", context)

@require_login
def update(request, curr_user, id):
	# Logic to check if curr_user is admin or user being updated
	if not (curr_user.admin or curr_user.id == int(id)):
		print(curr_user.id, id, curr_user.id == id)
		return redirect("/dashboard")

	# Logic to actually update
	errors = User.user_manager.update(id, request.POST)

	if errors:
		for error in errors:
			messages.error(request, error)
		return redirect("edit", id=id)
	else:
		return redirect("show", id=id)
