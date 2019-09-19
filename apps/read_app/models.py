from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors["name"] = "Name should be at least 2 characters"
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password_confirm'] != postData['password']:
            errors["password_confirm"] = "Passwords should match"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if check_if_email_exist(postData['email']) == True:
            errors['email'] = "Registered email should be unique"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email_address=postData['login_email'])
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['login_password'].encode(), logged_user.password.encode()):
                errors['login_password'] = "Password is incorrect!"
        else:
            errors['login_email'] = "User not exist!"
        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title should not be empty"
        if check_if_book_exist(postData['title']) == True:
            errors['title'] = "Book already exists"
        if len(postData['author']) < 2:
            errors["author"] = "Author name should be at least 2 characters"
        return errors


class ReviewManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['review']) < 1:
            errors["review"] = "Review should not be empty"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    # books
    # reviews


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
    # reviews

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, related_name = "reviews")
    user = models.ForeignKey(User, related_name = "reviews")
    objects = ReviewManager()

def check_if_email_exist(email_address):
    all_users = User.objects.all()
    for v in all_users:
        if email_address == v.email_address:
            return True
    return False

def check_if_book_exist(title):
    all_books = Book.objects.all()
    for v in all_books:
        if title == v.title:
            return True
    return False
