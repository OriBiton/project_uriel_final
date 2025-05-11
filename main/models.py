from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User

class PurchasedApartment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    building_number = models.CharField(max_length=10)
    floor_number = models.CharField(max_length=10, blank=True, null=True)
    apartment_number = models.CharField(max_length=10)

    def __str__(self):
        return f"דירה של {self.user.username} ב־{self.city}, {self.street} {self.building_number}, דירה {self.apartment_number}"

    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    building_number = models.CharField(max_length=10, blank=True, null=True)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    floor_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    street = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

class AvailableMeeting(models.Model):
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    location = models.CharField(max_length=255, verbose_name="מיקום הפגישה")  # שדה חדש

    def __str__(self):
        return f"{self.date} at {self.time}"

class BookedMeeting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meeting = models.ForeignKey(AvailableMeeting, on_delete=models.CASCADE)

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)


from django.db import models
from django.contrib.auth.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductOption(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class UserSelection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(ProductOption)

    def __str__(self):
        return f"בחירות של {self.user.username}"
