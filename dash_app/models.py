from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, form_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(form_data['rfname']) < 2:
            errors["rfname"] = "First name must be at least 2 characters!"
        if len(form_data['rlname']) < 2:
            errors["rlname"] = "Last name must be at least 2 characters!"
        if not email_regex.match(form_data['remail']):
            errors["remail"] = "Please enter valid email address!"
        if User.objects.filter(email= form_data['remail']).count() > 0:
            errors['usemail'] = "Sorry! This email is already in use by a user."
        if len(form_data['rpassword']) < 8:
            errors["rpassword"] = "Password must be at least 8 characters!"
        if form_data['rpassword'] != form_data['conpass']:
            errors['conpass'] = "Passwords must match!"
        return errors

    def login_validation(self, form_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(form_data['lemail']) or User.objects.filter(email= form_data['lemail']).count() == 0:
            errors["lemail"] = "We could not find a user with that email address!"
        if len(form_data['lpassword']) == 0:
            errors["lpassword"] = "Please enter correct password!"
        return errors

    def edit_accountvalid(self, form_data):
        errors ={}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(form_data['eemail']):
            errors["eemail"] = "Please enter valid email address!"
        if len(form_data['efname']) < 2:
            errors['efname'] = "Please enter First Name!"
        if len(form_data['elname']) < 2:
            errors['elname'] = "Please enter Last Name!"
        if User.objects.filter(email= form_data['eemail']).count() > 1:
            errors['ueemail'] = "Please use email that is not already in use!"
        return errors

class QuoteManager(models.Manager):
    def quote_validator(self, form_data):
        errors ={}
        if len(form_data['author']) < 3:
            errors['author'] = "Author's name should be at least 3 characters!"
        if len(form_data['quote']) < 10:
            errors['quote'] = "Quote must at least 10 characters!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #liked = a list of quotes this user likes
    #posted = a list of quotes this user posted
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=45)
    quote= models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="posted", on_delete = models.CASCADE)
    users_liked = models.ManyToManyField(User, related_name="liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
