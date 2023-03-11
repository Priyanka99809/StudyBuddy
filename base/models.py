from django.db import models
from django.contrib.auth.models import User


# Create your models here -room table /model in database

class Topic(models.Model):
    name=models.TextField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
     host= models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

     topic= models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)

     name=models.CharField(max_length=200)

     description=models.TextField(null=True,blank=True) #can be blank
     
     participants=models.ManyToManyField(User,related_name='participants',blank=True) # many to many reltionship with the model User but with another name participants
     
     updated=models.DateTimeField(auto_now=True) #info captured everytime room is updated
     created=models.DateTimeField(auto_now_add=True)  #info captured just once
     
     class Meta:
         ordering=['-updated','-created']  #newest most updated item will be first
     def __str__(self):
        return self.name
     
     
    
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)  #user model is already defined by django
    room=models.ForeignKey(Room,on_delete=models.CASCADE)  #each msg belongs to a room and if room gets deleted then delete message as well
    body=models.TextField()
    updated=models.DateTimeField(auto_now=True) 
    created= models.DateTimeField(auto_now_add=True)

    class Meta:
         ordering=['-updated','-created']  #newest most updated item will be first
         
    def __str__(self):   #getter
        return self.body[0:50] #so as to not clutter our admin pannel with messages
    
