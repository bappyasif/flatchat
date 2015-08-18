from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
# Creating a dummy model which stores info about users.
# Please note that we are using Class here.
class UserData(models.Model):
    user = models.OneToOneField(User)  # one to one key to user in django auth models.
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=12, null=True)  # We can store mobile number as a string.
    company = models.CharField(max_length=25, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.user.username


# This function will create UserData entry everytime a new user is added to Django.Contrib.auth.models. User
def user_post_save(sender, instance, created, **kwargs):
    """Create a user profile when a new user account is created"""
    if created == True:
        p = UserData()
        p.user = instance
        p.save()

# Calling above function with djnago signals(It take cares of async call).
post_save.connect(user_post_save, sender=User)


# This class is used to store keys, for signup, we will query for avaiblity of key here, if found then only user can
# signup.
class ApiKeys(models.Model):
    md5_key = models.CharField(max_length=32, unique=True)
    used_flag = models.BooleanField(default=False)  # If true: key is already used, else: key is available
    used_by = models.ForeignKey(User, null=True)    # if used_flag=True, set this to user instance who used that key.

    def __unicode__(self):
        return self.md5_key


