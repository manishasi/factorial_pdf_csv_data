from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
class fact(models.Model):
    value=models.IntegerField()
    factorial = models.IntegerField()
    def __str__(self):
        return str(self.id)

    

   
    
class factmulti(models.Model):
    factorial_id = models.ForeignKey(fact, on_delete=models.CASCADE, related_name='items')
    multifactorial=models.TextField()
    photo = models.ImageField(upload_to='pics/')

    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.photo))

