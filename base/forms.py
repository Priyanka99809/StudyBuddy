from django.forms import ModelForm  #already builtin form ready to add to room_form.html
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields= '__all__'  #create form based on all fields of room
        exclude= ['host','participants']  #dont add these two in create room form as host will be the one logged in
