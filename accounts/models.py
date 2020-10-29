from django.db import models

# Create your models here.
class details(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)


class token(models.Model):
    details = models.OneToOneField(to=details, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __unicode__(self):
        return self.token
