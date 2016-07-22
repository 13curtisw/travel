from __future__ import unicode_literals

from django.db import models
import bcrypt
import datetime

class UserManager(models.Manager):
	def loginValidation(self, username, password):
		errors = []
		if len(Users.objects.filter(username=username)) == 0:
			errors.append("Username does not exist in database")
		else:
			user = Users.objects.get(username=username)
			hashed = user.password
			password = password.encode('utf-8')
			hashed = hashed.encode('utf-8')
			if not bcrypt.hashpw(password, hashed) == hashed:
				errors.append("Invalid Password")
		return errors


		return len(Users.objects.filter(email=email)) > 0
	def getErrors(self, name, username, password, confirm_password):
		errors = []
		if len(name) < 3 or not name.isalpha():
			errors.append("Name is not valid (needs to be more than 2 characters and only alpha characters)")
		if len(username) < 3:
			errors.append("username must be more than 2 characters")
		if len(password) < 8:
			errors.append("Password needs to be at least 8 characters long")
		if not password == confirm_password:
			errors.append("Passwords must match")
		if len(Users.objects.filter(username=username)) > 0:
			errors.append("That username is already taken")
		return errors
	def encrypt(self, password):
		password = password.encode('utf-8')
		return bcrypt.hashpw(password, bcrypt.gensalt()) 
	def validPassword(self, password, hashed):
		password = password.encode('utf-8')
		hashed = hashed.encode('utf-8')
		if bcrypt.hashpw(password, hashed) == hashed:
			return True
		else:
			return False
class TripManager(models.Manager):
	def getErrors(self, destination, plan, startdate, enddate):
		errors = []
		if len(destination) < 1:
			errors.append("Destination field cannot be empty!")
		if len(plan) < 1:
			errors.append("Description field cannot be empty!")
		if len(startdate) < 1:
			errors.append("Date from field cannot be empty!")
		else:
			year = startdate[:4]
			month = startdate[5:7]
			day = startdate[8:]
			start = datetime.date(int(year), int(month), int(day))
			if start < datetime.date.today():
				errors.append("Start date must be in the future!")
		if len(enddate) < 1:
			errors.append("Date to field cannot be empty!")
		else:
			year = enddate[:4]
			month = enddate[5:7]
			day = enddate[8:]
			end = datetime.date(int(year), int(month), int(day))
			if end < datetime.date.today():
				errors.append("End date must be in the future!")
		if len(startdate) > 0 and len(enddate) > 0:
			if end < start:
				errors.append("Start date must be before end date!")
		return errors
	def convertToDate(self, date):
		year = date[:4]
		month = date[5:7]
		day = date[8:]
		newdate = datetime.date(int(year), int(month), int(day))
		return newdate


class Users(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	userManager = UserManager()
	objects = models.Manager()

class Trips(models.Model):
	destination = models.CharField(max_length=255)
	startdate = models.DateField()
	enddate = models.DateField()
	plan = models.TextField()
	users = models.ManyToManyField(Users, related_name="trips")
	tripManager = TripManager()
	objects = models.Manager()


