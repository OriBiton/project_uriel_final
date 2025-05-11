from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='תעודת זהות', max_length=9)
    password = forms.CharField(widget=forms.PasswordInput)

class CreateUserWithApartmentForm(forms.Form):
    # שדות משתמש
    username = forms.CharField(
        label='תעודת זהות', 
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='סיסמה',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    # שדות דירה
    city = forms.CharField(
        label='עיר', 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    street = forms.CharField(
        label='רחוב', 
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    building_number = forms.CharField(
        label='מספר בניין', 
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    floor_number = forms.CharField(
        label='קומה', 
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apartment_number = forms.CharField(
        label='מספר דירה', 
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class userProfileForm(forms.Form):
    first_name = forms.CharField(label='שם פרטי', max_length=30)
    last_name = forms.CharField(label='שם משפחה', max_length=30)
    email = forms.EmailField(label='אימייל')
    phone_number = forms.CharField(label='מספר טלפון', max_length=15, required=False)
    building_number = forms.CharField(label='מספר בניין', max_length=10, required=False)
    apartment_number = forms.CharField(label='מספר דירה', max_length=10, required=False)
    floor_number = forms.CharField(label='מספר קומה', max_length=10, required=False)
    city = forms.CharField(label='עיר', max_length=30, required=False)
    street = forms.CharField(label='רחוב', max_length=30, required=False)
    postal_code = forms.CharField(label='מיקוד', max_length=10, required=False)

from django import forms
from .models import AvailableMeeting, ContactMessage

class BookingForm(forms.Form):
    meeting = forms.ModelChoiceField(
        queryset=AvailableMeeting.objects.filter(is_booked=False),
        empty_label="בחר פגישה פנויה",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }

# forms.py
class AvailableMeetingForm(forms.ModelForm):
    class Meta:
        model = AvailableMeeting
        fields = ['date', 'time', 'location']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']