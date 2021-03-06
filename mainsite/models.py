from django.contrib.auth.models import AbstractUser
from django.db import models

class SiteUser(AbstractUser):
    description = models.TextField(default='I am me')
    pfpurl = models.TextField(default='https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg')
    def getinfo(self):
        return{
      
            "id":self.id,
            "username":self.username,
            "first_name":self.first_name,
            "email":self.email,
            "last_name":self.last_name,
            "profilepic": self.pfpurl,
            "description":self.description,
        }
class ReportedProblem(models.Model):
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField()
    problemtype = models.TextField()
    Severity = models.IntegerField()
    image = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    def getinfo(self):
        return{
      
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "problemtype":self.problemtype,
            "severity": self.Severity,
            "lat": self.latitude,
            "lng":self.longitude,
            "image":self.image,
            'type': self.problemtype
        }