from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q 
from django.contrib.auth.models import User  #contains user registered in admin panel
from .models import Room,Topic,Message
from .forms import RoomForm
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required #to restrict user from accessing certain pages
# Create your views here.

# rooms=[
#     { 'id':1,'name':'Let\'s Learn Python'},
#     { 'id':2,'name':'Design with me'},
#     { 'id':3,'name':'Frontend Developers'},
# ]


#view for login_register.html
def loginPage(request):
    #process info from user login
    page='login'
    if request.user.is_authenticated:  #if user is authenticated do not allow him to go to login page
        return redirect('home')
    if request.method== 'POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        #check if user exists
        try:
            user=User.objects.get(username=username)  #check if username is same as in username from admin panel
        except:
            messages.error(request,'User does not exist')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)   #user is now logged in
            return redirect('home')
        else:
            messages.error(request,'Username or Password is incorrect')
    context={'page':page}
    return render(request,'base/login_register.html',context)  #values in context can be used as variables in html file

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()

    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)  #not save now until user data is cleaned
            user.username=user.username.lower()
            user.save()   #now save the user to database
            login(request,user)   #user is now logged in  as well
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')
    return render(request,'base/login_register.html',{'form':form})


def home(request):
    q=request.GET.get('q')  if request.GET.get('q')!=None else ''
    #for search bar
    rooms=Room.objects.filter(   
        # search by topic name,room name or description of room using q which is passed through text input in navbar.html
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))
    
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))  #get the messages for only the particular topic and not every message for every room

    room_count=rooms.count()  #to get total no of rooms
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all() #show the most recent messages of the message model class
    
    participants=room.participants.all()  #get all participants
    #will only be executed if user writes a message
    if request.method=='POST':
        message=Message.objects.create(  #create an object of Message model class
            user=request.user, 
            body=request.POST.get('body'),
            room=room
        )
        room.participants.add(request.user) #add user to participants
        return redirect('room',pk=room.id)
    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

def userProfile(request,pk):
    user=User.objects.get(id=pk) #get the user from the USER built-in model
    rooms=user.room_set.all()  #get all rooms of user
    topics=Topic.objects.all()
    room_messages=user.message_set.all()  #get all messages of user
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


    
    #restrict user if he is not logged in
@login_required(login_url='login')  #redirect user to login page
def createRoom(request):
    form=RoomForm()

    if request.method=='POST':
        form=RoomForm(request.POST)  #collect form data in request.form to form and check if it is valid
        if form.is_valid():
            # form.save()
            room=form.save(commit=False)
            room.host=request.user  #host is logged in user as the roomform does not contain a host
            room.save()
            return redirect('home') #if form is valid then send user to home page

    context={'form':form} #dictionary object to pass data to template 
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')  #redirect user to login page
def updateRoom(request,pk):
    room=Room.objects.get(id=pk) #which room page to update eg 1 or 2 
    form=RoomForm(instance=room) #instance=room will show already existing values of the form
    
    if request.user!=room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)  #collect form data in request.form to form and check if it is valid
        if(form.is_valid()):
            form.save()
            return redirect('home')
    
    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')  #redirect user to login page
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST': #just delete room if request is made
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


@login_required(login_url='login')  #redirect user to login page
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)  #get the message
    if request.user!=message.user:  #if the deleter is not message owner
        return HttpResponse('You are not allowed here!!')
    if request.method=='POST': #just delete room if request is made
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


