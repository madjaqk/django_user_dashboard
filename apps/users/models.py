from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def validate_data(data):
	errors = []

	if len(data["first_name"]) < 2:
		errors.append("First name too short")
	elif not data["first_name"].isalpha():
		errors.append("First name contains non-letters")

	if len(data["last_name"]) < 2:
		errors.append("Last name too short")
	elif not data["last_name"].isalpha():
		errors.append("Last name contains non-letters")

	if not data["email"]:
		errors.append("E-mail missing")
	elif not EMAIL_REGEX.match(data["email"]):
		errors.append("Not a valid E-mail")

	if "password" in data:
		if data["password"] != data["confirm_password"]:
			errors.append("Password confirmation didn't match")

	return errors

class UserManager(models.Manager):
	def login(self, email, password):
		user = self.get(email=email)
		if not user:
			return False
		elif bcrypt.hashpw(password.encode("utf-8"), user.password.encode("utf-8")) != user.password.encode("utf-8"):
			return False
		else:
			return user

	def register(self, data):
		errors = validate_data(data)

		if self.filter(email=data["email"]):
			errors.append("E-mail in use")

		if len(data["password"]) < 8:
			errors.append("Password too short")

		if errors:
			return (False, errors)

		guy = User()
		guy.first_name = data["first_name"]
		guy.last_name = data["last_name"]
		guy.email = data["email"]
		if len(self.all()) == 0:
			guy.admin = True
		guy.password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
		guy.save()
		return (True, guy)

	def update(self, user_id, data):
		errors = validate_data(data)

		if "password" in data and data["password"]:
			if len(data["password"]) < 8:
				errors.append("Password too short")

		if errors:
			return errors

		user = self.get(id=user_id)
		user.first_name = data["first_name"]
		user.last_name = data["last_name"]
		user.email = data["email"]

		if "admin" in data:
			user.admin = data["admin"] == "True"

		user.description = data["description"]

		if "password" in data and data["password"]:
			user.password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

		user.save()
		return None

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	admin = models.BooleanField(default=False)
	description = models.TextField(default="", blank=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	user_manager = UserManager()

	def name(self):
		return "{} {}".format(self.first_name, self.last_name)
	
	def __str__(self):
		return "User with name {}".format(self.name())