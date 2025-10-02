from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)   
    description = models.TextField()           
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)   
    tags = models.CharField(max_length=250, blank=True, null=True)       

    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)     
    is_published = models.BooleanField(default=True)      

    def __str__(self):
        return self.title    