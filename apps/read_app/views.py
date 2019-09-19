from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book, Review
from datetime import datetime
import bcrypt

def index(request):
    return render(request, "read_app/index.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags="register_error")
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            request.session['alias'] = request.POST['alias']
            request.session['email'] = request.POST['email']
            User.objects.create(name=request.POST['name'], alias=request.POST['alias'],
            email_address=request.POST['email'],password=pw_hash)
            return redirect('/books')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login_error")
        return redirect('/')
    else:
        user = User.objects.filter(email_address=request.POST['login_email'])
        logged_user = user[0]
        request.session['alias'] = logged_user.alias
        request.session['email'] = logged_user.email_address
        return redirect('/books')

def book_home(request):
    context = {
        "latest_three_reviews": Review.objects.all().order_by("-id")[:3],
        "all_books": Book.objects.all(),
    }
    return render(request, "read_app/book_home.html", context)

def add_book(request):
    return render(request, "read_app/add_book.html")

def new_book(request):
    this_user = User.objects.get(email_address=request.session['email'])
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books/add')
    else:  
        this_book = Book.objects.create(title=request.POST['title'], author=request.POST['author'], user=this_user)
        this_book.save()
        Review.objects.create(review=request.POST['review'],rating=request.POST['rating'],user=this_user,book=this_book)
        return redirect('/books/' + str(this_book.id))

def one_book(request,num):
    context = {
        "this_book": Book.objects.get(id=num),
    }
    return render(request, "read_app/one_book.html", context)

def add_review(request,num):
    this_user = User.objects.get(email_address=request.session['email'])
    this_book = Book.objects.get(id=num)
    errors = Review.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books/' + num)
    else:
        Review.objects.create(review=request.POST['review'],rating=request.POST['rating'],user=this_user,book=this_book)
        return redirect('/books/' + num)
    

def delete_review(request,num):
    this_review = Review.objects.get(id=num)
    this_review.delete()
    return redirect('/books/' + str(this_review.book.id))

def user_page(request,num):
    context = {
        "this_user": User.objects.get(id=num),
    }
    return render(request, "read_app/user_page.html", context)



def logout(request):
    del request.session['alias']
    del request.session['email']
    return redirect('/')