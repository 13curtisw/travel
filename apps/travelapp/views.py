from django.shortcuts import render, HttpResponse, redirect
from .models import Users, UserManager, Trips, TripManager
from django.core.urlresolvers import reverse

def index(request):
	return render(request,'travelapp/index.html')
def login(request):
	username = request.POST['username']
	password = request.POST['password']
	errors = Users.userManager.loginValidation(username, password)
	if len(errors) == 0:
		user = Users.objects.get(username=username)
		request.session['id'] = user.id
		return redirect(reverse('travel_home'))
	else:
		context = {
			"regerrors": [],
			"logerrors": errors
		}
		return render(request, 'travelapp/index.html', context)
def register(request):
	name = request.POST['name']
	username = request.POST['username']
	password = request.POST['password']
	confirm_password = request.POST['confirm_password']
	errors = Users.userManager.getErrors(name, username, password, confirm_password)
	print errors
	if len(errors) == 0:
		encryptedPassword = Users.userManager.encrypt(password)
		user = Users.objects.create(name=name, username=username, password=encryptedPassword)
		request.session['id'] = user.id
		return redirect(reverse('travel_home'))
	else:
		context = {
			'regerrors': errors,
			'logerrors': []
		}
		return render(request,'travelapp/index.html', context)
def logout(request):
	request.session.pop('id')
	return redirect(reverse('travel_start'))

def home(request):
	user = Users.objects.get(id=request.session['id'])
	print Trips.objects.all()
	context = {
		"user": user,
		"usertrips": user.trips.all(),
		"othertrips": Trips.objects.exclude(users=user),
	}
	return render(request, 'travelapp/home.html', context)
def add(request):
	return render(request, 'travelapp/add.html')
def create(request):
	destination = request.POST['destination']
	plan = request.POST['plan']
	startdate = request.POST['startdate']
	enddate = request.POST['enddate']
	errors = Trips.tripManager.getErrors(destination, plan, startdate, enddate)
	if len(errors) == 0:
		trip = Trips.objects.create(destination=destination, plan=plan, startdate=Trips.tripManager.convertToDate(startdate), enddate=Trips.tripManager.convertToDate(enddate))
		user = Users.objects.get(id=request.session['id'])
		print user.name
		trip.users.add(user)
		trip.save()
		return redirect(reverse('travel_home'))
	else:
		context = {
			'errors': errors
		}
		return render(request, 'travelapp/add.html', context)
def update(request, id):
	trip = Trips.objects.get(id=id)
	trip.users.add(Users.objects.get(id=request.session['id']))
	trip.save()
	return redirect(reverse('travel_home'))
def show(request, id):
	otherusers = Trips.objects.get(id=id).users.exclude(id=Trips.objects.get(id=id).users.all()[0].id)
	context = {
		'trip': Trips.objects.get(id=id),
		'otherusers': otherusers
	}
	return render(request, 'travelapp/show.html', context)













