from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def user_val(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = 'You must enter a first name!'
        if len(postData['last_name']) < 2:
            errors["last_name"] = 'You must enter a last name!'
        if len(postData['email']) < 1:
            errors["email"] = 'You must enter an email!'
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = 'You must use proper email syntax!'
        if len(User.objects.filter(email = postData['email'])):
            errors["email"] = 'Email already exists'
        if len(postData['password']) < 8:
            errors["password"] = 'Your password must be at least 8 characters!'
        if postData['password_conf'] != postData['password']:
            errors["password_conf"] = 'Your passwords must match!'
        return errors

class FoodManager(models.Manager):
    def food_val(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = 'You must enter a food name!'
        if len(postData['calories']) < 1:
            errors["calories"] = 'You must enter food calories!'
        if len(postData['carbs']) < 1:
            errors["carbs"] = 'You must enter carbs!'
        if len(postData['fats']) < 1:
            errors["fats"] = 'You must enter fats!'
        if len(postData['proteins']) < 1:
            errors["proteins"] = 'You must enter proteins!'
        return errors 

class WorkoutManager(models.Manager):
    def workout_val(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = 'You must enter a workout name!'
        if len(postData['description']) < 1:
            errors["description"] = 'You must enter a description!'
        return errors 

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Food(models.Model):
    name = models.CharField(max_length=255)
    calories = models.CharField(max_length=255)
    carbs= models.CharField(max_length=255)
    fats = models.CharField(max_length=255)
    proteins = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="foods")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = FoodManager()

class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    repetitions = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="workouts")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = WorkoutManager()
    
class WorkoutLog(models.Model):
    notes = models.CharField(max_length=500)
    workout = models.ForeignKey(Workout, related_name="workoutlog")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)



