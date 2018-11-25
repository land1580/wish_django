from django.db import models
import re, bcrypt, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validate(self, post_attempt):
        first_name = post_attempt['first_name']
        last_name = post_attempt['last_name']
        email = post_attempt['email']
        password = post_attempt['password']
        pw_confirm = post_attempt['pw_confirm']
        user = User.objects.all().values().filter(email = email)
        errors = {}

        if len(first_name) < 2:
            errors["first_name"] = "TOO SHORT! First name must be at least 2 characters long"
        if len(last_name) < 2:
            errors["last_name"] = "TOO SHORT! Last name must be at least 2 characters long"
        if not EMAIL_REGEX.match(email):
            errors["email"] = "EMAIL INVALID! Check format or try another email"
        if len(password) < 5:
            errors["password"] = "TOO SHORT! Passwords must be at least 5 characters long"
        if password != pw_confirm:
            errors["pw_confirm"] = "MATCH ERROR! Passwords don't match"
        if user:
            errors["user"] = "EXISTING EMAIL! Email already in use"
        return errors

    def login_check(self, post_attempt):
        email = post_attempt['email']
        password = post_attempt['password']
        errors = {}

        try:
            user = User.objects.all().values().get(email = email)
            if user:
                if bcrypt.checkpw(password.encode(), user['pw_hash'].encode()):
                    print("Success!")
                else:
                    errors["password"] = "MATCH ERROR! Email/Password combination is incorrect"
                return errors
        except:
            errors["login"] = "MATCH ERROR! Email/Password combination is incorrect"
        return errors

    def make_new_user(self, post_attempt):
        user = self.create(
            first_name = post_attempt['first_name'],
            last_name = post_attempt['last_name'],
            email = post_attempt['email'],
            pw_hash = bcrypt.hashpw(post_attempt['password'].encode(), bcrypt.gensalt())
        )
        return user

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    pw_hash = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()



class WishManager(models.Manager):
    def validation(self, post_attempt):
        item = post_attempt['item']
        description = post_attempt['description']
        errors = {}

        if len(item) < 3:
            errors["item"] = "TOO SHORT! Item must be at least 3 characters long"
        if len(item) > 100:
            errors["item"] = "TOO LONG! Fields must be less than 100 characters long"
        if len(description) < 3:
            errors["description"] = "TOO SHORT! Description must be at least 3 characters long"
        if len(description) > 100:
            errors["description"] = "TOO LONG! Fields must be less than 100 characters long"
        return errors

    def new_wish(self, post_attempt, user):
        curr_user = User.objects.get(email = user.email)
        Wish.objects.create(item = post_attempt['item'], description = post_attempt['description'], creator = curr_user)

    def edit_wish(self, post_attempt, wish_id):
        item = post_attempt['item']
        description = post_attempt['description']
        curr_wish = Wish.objects.get(id = wish_id)

        curr_wish.item = item
        curr_wish.description = description
        curr_wish.save()

    def destroy_wish(self, wish_id):
        curr_wish = Wish.objects.get(id = wish_id)
        curr_wish.delete()

class Wish(models.Model):
    item = models.CharField(max_length = 255)
    description = models.CharField(max_length = 500)
    granted = models.BooleanField(default = False)
    creator = models.ForeignKey(User,related_name = 'posts')
    likes = models.ManyToManyField(User, related_name = 'liked')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = WishManager()
