from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import available_attrs
from django.core.exceptions import ObjectDoesNotExist
from .models import User

def require_login(view_func):
	@wraps(view_func, assigned=available_attrs(view_func))
	def _wrapped_view(request, *args, **kwargs):
		try:
			curr_user = User.user_manager.get(id=request.session["curr_user"])
		except (KeyError, ObjectDoesNotExist):
			messages.error(request, "You must be logged in to view this page")
			return redirect("login_page")
		
		return view_func(request, curr_user, *args, **kwargs)
	return _wrapped_view