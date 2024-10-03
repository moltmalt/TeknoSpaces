from django.db import models

# Create your models here.
class Space(models.Model):
     main_image_url = models.CharField(max_length=500)
     second_image_url = models.CharField(max_length=500)
     third_image_url = models.CharField(max_length=500)
     fourth_image_url = models.CharField(max_length=500)
     fifth_image_url = models.CharField(max_length=500)
     sixth_image_url = models.CharField(max_length=500)
     title = models.CharField(max_length=100)
     description = models.CharField(max_length=500)
     type = models.CharField(max_length=100)
     venue = models.CharField(max_length=100)
     tag = models.CharField(max_length=100)
     schedule = models.CharField(max_length=16)
     seating_capacity = models.IntegerField() 
     has_air_conditioner = models.BooleanField()
     has_internet = models.BooleanField()
     has_television = models.BooleanField()

     def __str__(self):
          return self.title