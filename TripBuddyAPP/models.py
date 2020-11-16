from django.db import models
from django.contrib import messages
from datetime import date
import hashlib, bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self,posD):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(posD['fname_']) == 0:
            errors['fnamerq'] = 'First Name is required'
        elif len(posD['fname_']) <3:
            errors['fnamemin'] = 'First Name must be at least 3 characters'
        if len(posD['email_']) == 0:
            errors['emailrq'] = 'Email is required'
        if not EMAIL_REGEX.match(posD['email_']):            
            errors['emailinvalid'] = "Invalid email address!"            
        elif posD['email_'] in User.objects.all().values_list('email', flat=True):
            errors['duplicate_email'] = "This Email has already been used"        
        if len(posD['pwd_']) == 0:
            errors['pwdrq'] = 'Password is required'
        elif len(posD['pwd_']) <8:
            errors['pwdmin'] = 'Password must be at least 8 characters'
        if posD['pwd_'] != posD['cpwd_']:
            errors['pwdmatch'] = 'Passwords do not match!'
        if len(posD['lname_']) == 0:
            errors['lnamerq'] = 'Last Name is required'
        elif len(posD['lname_']) <3:
            errors['lnamemin'] = 'Last Name must be at least 3 characters' 

        return errors
    
    def login_validator(self,posD):
        errors ={}
        user = User.objects.filter(email=posD['email_'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if not user:
            errors['usr_reg'] = 'Please register first!'
        
            
            
        else:
            loginuser = user[0]
            prehashpwd = hashlib.sha256(posD['pwd_'].encode()).hexdigest()
            if not bcrypt.checkpw(prehashpwd.encode(), loginuser.pwd.encode()):
                errors['pwd_notmatch'] = 'Password is incorrect!'
                
        
        return errors

class TripManager(models.Manager):
    def trip_validator(self,posD):
        errors = {}
        today = date.today().strftime('%Y-%m-%d')
        if len(posD['new_des']) == 0:
            errors['desreq'] = 'Destination is required'
        if len(posD['new_desc']) == 0:
            errors['descreq'] = 'Description is required'
        if len(posD['new_sdate']) == 0:
            errors['sdatereq'] = 'Start Date is required'
        elif posD['new_sdate'] < today:
            errors['sdatefuture'] = 'Start Date must be future date'
        if len(posD['new_edate']) == 0:
            errors['edatereq'] = 'End Date is required'
        elif posD['new_edate'] < today:
            errors['edatefuture'] = 'End Date must be future date'
        if posD['new_edate'] < posD['new_sdate']:
            errors['dateinvalid'] = 'End Date should not be before Start Date'
        return errors
        

class User(models.Model):
    fname = models.CharField(max_length = 255)
    lname = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    pwd = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return f"<User object: {self.fname} ({self.id})>"

class Trip(models.Model):
    DateFormat = ['%Y-%m-%d']
    des = models.CharField(max_length = 255)
    desc = models.CharField(max_length = 255)
    planner = models.ForeignKey(User, related_name="trips", on_delete = models.CASCADE)
    joiner = models.ManyToManyField(User, related_name="jointrips")
    sdate = models.DateTimeField()
    edate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()

    def __str__(self):
        return f"<Trip object: {self.des} ({self.id})>"