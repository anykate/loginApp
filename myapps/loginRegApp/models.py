from django.db import models
import re


# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}

        # Email REGEX: ^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$'
        )

        if len(post_data['fname']) < 1:
            errors['fname'] = 'First Name is required'
        if len(post_data['lname']) < 1:
            errors['lname'] = 'Last Name is required'

        if len(post_data['email']) < 1:
            errors['email'] = 'Email is required'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email_pattern'] = 'Invalid Email Address'
        else:
            email_match = User.objects.filter(email=post_data['email'])
            if email_match:
                errors['email_match'] = 'User already exists'

        if len(post_data['pwd']) < 8:
            errors['pwd'] = 'Password is required and should be at least 8 characters long'
        if len(post_data['c_pwd']) < 8:
            errors['c_pwd'] = 'Confirm Password is required and should be at least 8 characters long'
        elif post_data['pwd'] != post_data['c_pwd']:
            errors['c_pwd'] = 'Password and Confirm Password fields must match'

        # print(errors)
        return errors

    def login_validator(self, post_data):
        pass


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.email
