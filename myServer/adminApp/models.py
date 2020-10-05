from django.db import models
import uuid
import scriptTools.timeTools as tTools
from scriptTools.charLength import charlen, longercharlen


# admin表，用于验证管理员
class AdminInfo(models.Model):
  admin_id = models.AutoField(primary_key=True, auto_created=True)
  admin_uuid = models.CharField(default="", blank=True, max_length=charlen)
  admin_tele = models.CharField(unique=True, max_length=charlen)
  admin_pwd = models.CharField(default="", blank=True, max_length=charlen)
