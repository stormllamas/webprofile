from django.db import models
from solo.models import SingletonModel
from django.utils import timezone

import sys
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

class Contact(models.Model):
  name = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  phone = models.CharField(max_length=50, blank=True, null=True)
  subject = models.CharField(max_length=200)
  message = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=timezone.now, blank=True)
  user_id = models.IntegerField(blank=True, null=True)

class SiteConfiguration(SingletonModel):
  site_name = models.CharField(max_length=255, default='Site Name')
  resume = models.FileField(upload_to='photos/%Y/%m/%d/', blank=True)
  maintenance_mode = models.BooleanField(default=False)

  def __unicode__(self):
    return u"Site Configuration"