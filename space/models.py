from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
 
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Space(models.Model):
    main_image = models.ImageField(upload_to='space_images', blank=True, null=True)
    second_image = models.ImageField(upload_to='space_images', blank=True, null=True)
    third_image = models.ImageField(upload_to='space_images', blank=True, null=True)
    fourth_image = models.ImageField(upload_to='space_images', blank=True, null=True)
    fifth_image = models.ImageField(upload_to='space_images', blank=True, null=True)
    sixth_image = models.ImageField(upload_to='space_images', blank=True, null=True)
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category, related_name='space')
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    managed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='spaces', blank=True, null=True, on_delete=models.RESTRICT)
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='space', blank=True, null=True, on_delete=models.SET_NULL)
    is_booked = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    book_count = models.IntegerField(null=True, blank=True, default=0)

    type = models.ManyToManyField(Type, related_name='space')
    venue = models.CharField(max_length=100)
    schedule = models.CharField(max_length= 16, null=True, blank=True, default='abcdefghijklmnop')
    seating_capacity = models.IntegerField() 
    hasAirConditioner = models.BooleanField()
    hasInternet = models.BooleanField()
    hasTelevision = models.BooleanField()

    def __str__(self):
        return self.title
