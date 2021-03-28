from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Quote, User
import bcrypt

def index(request):
    print("*"*10, "I am inside the index function", "*"*10)
    if 'email' not in request.session:
        return render(request, "login_reg.html")
    return redirect('/quotes')
    

def register(request):
    print("*"*10, "I am inside the register function", "*"*10)
    password = request.POST['rpassword']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    print(pw_hash)
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'rfname':
                messages.error(request, value, extra_tags='rfname')
            if key == 'rlname':
                messages.error(request, value, extra_tags='rlname')
            if key == 'remail':
                messages.error(request, value, extra_tags='remail')
            if key == 'usemail':
                messages.error(request, value, extra_tags='usemail')
            if key == 'rpassword':
                messages.error(request, value, extra_tags='rpassword')
            if key == 'conpass':
                messages.error(request, value, extra_tags='conpass')
        return redirect('/')
    else:
        newuser = User.objects.create(
            first_name = request.POST['rfname'],
            last_name = request.POST['rlname'],
            email = request.POST['remail'],
            password = pw_hash
            )
        print("*"*10, newuser.id, "*"*10)
        request.session['id'] = newuser.id
        request.session['email'] = newuser.email
        request.session['fname'] = newuser.first_name
        request.session['lname'] = newuser.last_name
        print("*"*10, request.session['email'], "*"*10) 
        return redirect('/quotes')

def login(request):
    print("*"*10, "I am inside the login function", "*"*10)
    errors = User.objects.login_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'lemail':
                messages.error(request, value, extra_tags='lemail')
            if key == 'lpassword':
                messages.error(request, value, extra_tags='lpassword')
        print("*"*10, "You are being redirected back to root route", "*"*10)
        return redirect('/')
    user = User.objects.filter(email=request.POST['lemail'])
    if user: # note that we take advantage of truthiness here: an empty list will return false
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['lpassword'].encode(), logged_user.password.encode()):
            request.session['id'] = logged_user.id
            request.session['email'] = logged_user.email
            request.session['fname'] = logged_user.first_name
            request.session['lname'] = logged_user.last_name
            return redirect('/quotes')
    return redirect("/")

def quotes(request):
    print("*"*10, "I am inside the quotes function", "*"*10)
    if 'email' in request.session:
        print("*"*10, "User in session", "*"*10)
        context = {
        "quotes": Quote.objects.all()
    }
        return render(request, "quotes.html", context)
    else:
        return redirect('/')

def addquote(request):
    print("*"*10, "I am inside the login function", "*"*10)
    user = User.objects.get(id=request.session['id'])
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'author':
                messages.error(request, value, extra_tags='author')
            if key == 'quote':
                messages.error(request, value, extra_tags='quote')
        print("*"*10, "You are being redirected back to quotes page", "*"*10)
        return redirect('/quotes')
    else:
        newquote = Quote.objects.create(
            author = request.POST['author'],
            quote = request.POST['quote'],
            posted_by = user
        )
        print("*"*10, newquote, "*"*10)
        print("*"*10, "You are being redirected back to quotes page", "*"*10)
        return redirect('/quotes')

def account(request, user_id):
    print("*"*10, "I am inside the account function", "*"*10)
    if 'email' in request.session:
        print("*"*10, "User in session", "*"*10)
        return render(request, "edit.html")
    else:
        return redirect('/')

def edit(request):
    print("*"*10, "I am inside the account function", "*"*10)
    upuser = User.objects.get(id=request.session['id'])
    errors = User.objects.edit_accountvalid(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'efname':
                messages.error(request, value, extra_tags='efname')
            if key == 'elname':
                messages.error(request, value, extra_tags='elname')
            if key == 'eemail':
                messages.error(request, value, extra_tags='eemail')
            if key == 'ueemail':
                messages.error(request, value, extra_tags='ueemail')
        print("*"*10, "You are being redirected back to the edit page", "*"*10)
        return redirect(f"/myaccount/{request.session['id']}")
    else:
        upuser.first_name = request.POST['efname']
        upuser.last_name = request.POST['elname']
        upuser.email = request.POST['eemail']
        upuser.save()
        messages.success(request, "Your account was successfully updated!")
        return redirect(f"/myaccount/{request.session['id']}")

def userquotes(request, user_id):
    print("*"*10, "I am inside the userquotes function", "*"*10)
    if 'email' in request.session:
        user = User.objects.get(id= user_id)
        print("*"*10, "User in session", "*"*10)
        content = {
            "user":  User.objects.get(id= user_id),
            "quotes": Quote.objects.filter(posted_by= User.objects.get(id=user_id))
        }
        return render(request, "user_quotes.html", content)
    else:
        return redirect('/')

def likequote(request, quote_id):
    print("*"*10, "I am inside the likequote function", "*"*10)
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id= request.session['id'])
    if quote.users_liked.filter(id=user.id).exists():
        quote.users_liked.remove(user)
        liked = False
    else:
        quote.users_liked.add(user)
        liked = True
    quote.save()
    print("*"*10, quote.quote, "*"*10)
    return redirect('/quotes')

def success(request):
    print("*"*10, "I am inside the success function", "*"*10)
    if 'email' in request.session:
        print("*"*10, "User in session", "*"*10)
        return render(request, "success.html")
    else:
        return redirect('/')

def logout(request):
    print("*"*10, "I am inside the logout function", "*"*10)
    request.session.flush()
    return redirect('/')


