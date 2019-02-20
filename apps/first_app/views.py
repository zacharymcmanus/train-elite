from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import date
import json
import requests
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Renders
def index(request):
    return render(request, "first_app/index.html")

def dashboard(request): 
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id=request.session['id'])
        creator = Workout.objects.filter(creator_id=request.session['id'])
        todays_workout = Workout.objects.filter(created_at__date=date.today())
        todays_food = Food.objects.filter(created_at__date=date.today())
        print("got todays workout", todays_workout)
        context = {
            'user': user,
            'creator': creator,
            'todays_workout': todays_workout,
            'todays_food': todays_food
        }
        return render(request, "first_app/dashboard.html", context)

def login(request):
    return render(request, "first_app/loginuser.html")

def register(request):
    return render(request, "first_app/registeruser.html")

def workouts(request):
    workout = Workout.objects.all()
    creator = Workout.objects.filter(creator_id=request.session['id'])
    user = User.objects.get(id=request.session['id'])
    print("got workout objects", workout)

    # paginator = Paginator(workout, 1)
    # page = request.GET.get('page')
    # try:
    #     items = paginator.page(page)
    # except PageNotAnInteger:
    #     items = paginator.page(1)
    # except EmptyPage:
    #     items = paginator.page(paginator.num_pages)

    context = { 
        'workout': workout,
        'user': user,
        'creator': creator
    }
    return render(request, "first_app/workout.html", context)

def view_workout(request):
    workout = Workout.objects.all()
    creator = Workout.objects.filter(creator_id=request.session['id'])
    user = User.objects.get(id=request.session['id'])
    print("got workout objects", workout)
    context = { 
        'workout': workout,
        'user': user,
        'creator': creator
    }
    return render(request, "first_app/viewworkout.html", context)

def nutrition(request):
    creator = Food.objects.filter(creator_id=request.session['id'])
    user = User.objects.get(id=request.session['id'])
    context = {
        'creator': creator,
        'user': user,
    }
    return render(request, "first_app/food.html", context)


def edit_account(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user
    }
    return render(request, "first_app/editaccount.html", context)

def search_workout(request):
    creator = Workout.objects.filter(creator_id=request.session['id'])
    context = {
        'creator': creator
    }
    return render(request, "first_app/search.html", context)

def profile(request):
    user = User.objects.get(id=request.session['id'])
    context = { 
        'user': user
    }
    return render(request, "first_app/profile.html", context)
    
# Posts
def add_workout(request):
    if request.method == 'POST':
        Workout.objects.create(name=request.POST['name'], description=request.POST['description'], weight=request.POST['weight'], repetitions=request.POST['repetitions'], time=request.POST['time'], creator=User.objects.get(id= request.session['id']))
        print ("successfully added workout")
        return redirect('/workouts')

def view_workout(request, id):
    workout = Workout.objects.get(id=id)
    context = {
        'workout': workout,
    }
    return render(request, "first_app/viewworkout.html", context)

def delete_workout(request, id):
    workout_to_delete = Workout.objects.filter(id=id)
    workout_to_delete.delete()
    return redirect('/workouts')

def add_food(request):
    if request.method == 'POST':
        print("in addfood function")
        Food.objects.create(name=request.POST['name'], calories=request.POST['calories'], carbs=request.POST['carbs'], fats=request.POST['fats'], proteins=request.POST['proteins'], creator=User.objects.get(id= request.session['id']))
        print ("successfully added food")
        return redirect('/nutrition')

def delete_food(request, id):
    food_to_delete = Food.objects.filter(id=id)
    food_to_delete.delete()
    return redirect('/dashboard')

def register_user(request):
    if request.method == 'POST':
        errors = User.objects.user_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='registration_errors')
            return redirect('/registerpage')
        else: 
            password_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=password_hash)
            user = User.objects.get(email=request.POST['email'])
            request.session['first_name'] = user.first_name
            request.session['id'] = user.id
            print ("==========successfully registered========")
            return redirect('/dashboard')    

def login_user(request):
    user = User.objects.filter(email=request.POST['email'])
    if not len(user):
        return redirect('/login')
    if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
        user_login = User.objects.get(email=request.POST['email'])
        request.session['first_name'] = user_login.first_name
        request.session['id'] = user_login.id
        return redirect('/dashboard')
    else:
        return redirect('/login')

def edit_user_account(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        user.first_name=request.POST['first_name']
        user.last_name=request.POST['last_name']
        user.email=request.POST['email']
        user.save()
        print ("successfully updated user account!")
        return redirect('/account/edit') 

def logout_user(request):
    request.session.clear()
    return redirect('/')

def search_workouts(request):
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch: 
            match = Workout.objects.filter(name__icontains=srch)
            if match: 
                print ("got match!", match)
            else: 
                print("no match found")
                messages.error(request, 'No result found!')
        else: 
            return redirect('/workouts')
    
    user = User.objects.get(id=request.session['id'])
    creator = Workout.objects.filter(creator_id=request.session['id'])
    context = {
        'creator': creator,
        'user': user,
        'sr': match
    }
    return render(request, "first_app/workout.html", context)

def edit_workout(request, id):
    if request.method == 'POST':
        errors = Workout.objects.workout_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='editworkouterrors')
            return redirect('/workoutpage')
        else:
            workout = Workout.objects.get(id=id)
            workout.name=request.POST['name']
            workout.description=request.POST['description']
            workout.weight=request.POST['weight']
            workout.repetitions=request.POST['repetitions']
            workout.time=request.POST['time']
            workout.save()
            return redirect('/workouts')

def edit_food(request):
    if request.method == 'POST':
        errors = Food.objects.food_val(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags='editfooderrors')
            return redirect('/foodpage')
        else:
            food = Food.objects.get(id=id)
            food.name=request.POST['name']
            food.calories=request.POST['calories']
            food.carbs=request.POST['carbs']
            food.fats=request.POST['fats']
            food.proteins=request.POST['proteins']
            food.save()
            return redirect('/foodpage')












