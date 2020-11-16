from django.shortcuts import render,redirect
from django.contrib import messages
import hashlib, bcrypt
from datetime import date
from .models import * 

# Create your views here.
def index(request):            
    return render(request,'index.html')

def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)
    print('ERROR'*20,errors)
    if len(errors) > 0:
        for key,value in errors.items():
            if key.find('usr') >=0 :
                messages.error(request,value, extra_tags='usr login')
                
            else:                
                messages.error(request,value, extra_tags='pwd login')
        request.session['temp'] = request.POST['email_']        
        return redirect('/')
    else:
        request.session['loggedin'] = User.objects.get(email = request.POST['email_']).id
        return redirect('/travels')
    
def register(request):
    print(request.POST)
    # validate user register
    errors = User.objects.register_validator(request.POST)
    print('ERROR HERE','*'*20)
    print(errors)
    if len(errors) > 0:
        for key,value in errors.items():
            if key.find('fname') >=0:
                messages.error(request,value,extra_tags='fname')
            elif key.find('email') >=0:
                messages.error(request,value,extra_tags='email')
            elif key.find('pwd') >=0:
                messages.error(request,value,extra_tags='pwd')
            else:
                messages.error(request,value,extra_tags='lname')           
        request.session['regtemp_fname'] = request.POST['fname_']
        request.session['regtemp_email'] = request.POST['email_']
        request.session['regtemp_lname'] = request.POST['lname_']                
        return redirect('/')
    else:
    # register new user
        prehashpwd = hashlib.sha256(request.POST['pwd_'].encode()).hexdigest()
        bpwd = bcrypt.hashpw(prehashpwd.encode(), bcrypt.gensalt()).decode()
        # if hashlib.sha256(request.POST['cpwd_'].encode()).hexdigest() == hashed:
        #     print('/'*20, hashed)
        newuser = User.objects.create(fname = request.POST['fname_'], email = request.POST['email_'], pwd = bpwd, lname = request.POST['lname_'])
        request.session['loggedin'] = newuser.id
        return redirect('/travels')

def success(request):
    if not 'loggedin' in request.session:
        messages.error(request,'Please log in',extra_tags = 'usr login')        
        return redirect('/')
    else:
        trip_by_user = Trip.objects.filter(planner = User.objects.get(id=int(request.session['loggedin'])))
        join_trip = User.objects.get(id = int(request.session['loggedin'])).jointrips.all()
        print('TRIP BY USER'*3,trip_by_user)
        print('*'*20,join_trip)
        trips = trip_by_user | join_trip
                
        print('#'*20,join_trip)
        context = {
        'currentuser' : User.objects.get(id = request.session['loggedin']),
        'join_trips' : User.objects.get(id = int(request.session['loggedin'])).jointrips.all(),
        'other_trips': Trip.objects.exclude(joiner = int(request.session['loggedin'])),
        'trip_by_user': trip_by_user,
        'all' : Trip.objects.all(),
        }

        return render(request,'travels.html',context)

def logout(request):
    if not 'loggedin' in request.session:
        return redirect('/')
    else:
        request.session.clear()
        return redirect('/')

def create(request):
    if not 'loggedin' in request.session:
        messages.error(request,'Please log in',extra_tags = 'usr login')        
        return redirect('/')
    else:
        return render(request, 'newtrip.html')

def new(request):
    if not 'loggedin' in request.session:
        messages.error(request,'Please log in',extra_tags = 'usr login')        
        return redirect('/')
    else:
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/addtrip')
        else:
            Trip.objects.create(des = request.POST['new_des'],desc = request.POST['new_desc'],sdate = request.POST['new_sdate'],edate = request.POST['new_edate'], planner = User.objects.get(id=int(request.session['loggedin'])))
                
            return redirect('/travels')

def tripinfo(request,tripID):
    if not 'loggedin' in request.session:
        messages.error(request,'Please log in',extra_tags = 'usr login')        
        return redirect('/')
    else:
        print(Trip.objects.get(id=tripID).joiner.all())
        context = {
            'view_trip' : Trip.objects.get(id=tripID),
            'alljoiners' : Trip.objects.get(id=tripID).joiner.all(),
        }
        return render(request,'tripinfo.html',context)

def join(request,tripID):
    if not 'loggedin' in request.session:
        messages.error(request,'Please log in',extra_tags = 'usr login')        
        return redirect('/')
    else:
        join_trip = Trip.objects.get(id=tripID)
        User.objects.get(id=int(request.session['loggedin'])).jointrips.add(join_trip)
        return redirect('/travels')

def cancel(request,tripID):
    if not 'loggedin' in request.session:
        messages.error(request,'Please log in',extra_tags = 'usr login')        
        return redirect('/')
    else:
        cancel_trip = Trip.objects.get(id=tripID)
        User.objects.get(id=int(request.session['loggedin'])).jointrips.remove(cancel_trip)
        return redirect('/travels')

def delete(request,tripID):
    if not 'loggedin' in request.session:
        messages.error(request,'Please log in',extra_tags = 'usr login')        
        return redirect('/')
    else:
        del_trip = Trip.objects.get(id=tripID)
        del_trip.delete()
        return redirect('/travels')


