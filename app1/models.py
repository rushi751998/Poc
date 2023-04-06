from django.db import models
from .validators import file_size

# Create your models here.
# class Video(models.Model):
#     caption=models.DateField(default="NA")
#     video=models.FileField(upload_to="video")
#     processed_video=models.FileField(upload_to="processed_video",default="Na")

#     def __str__(self):
#         return self.caption
    
class Video2(models.Model):
    caption=models.DateField(default="NA")
    video=models.FileField(upload_to="video")
    processed_video=models.FileField(upload_to="processed_video",default="Na")

    def __str__(self):
        return (f'{self.caption}')
    
    
class person_db(models.Model):
    face_id = models.IntegerField(default=-0)
    gender = models.CharField(max_length=10,default="")
    age = models.IntegerField(default=-0)
    emotion = models.CharField(max_length=20,default="")
    race = models.CharField(max_length=30,default="")
    image = models.ImageField(upload_to ='images',default="")
    
    def __str__(self):
        return f"{self.face_id} - {self.gender} - {self.age} - {self.emotion}"
    
    