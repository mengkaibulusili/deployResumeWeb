from django.db import models
import uuid
import scriptTools.timeTools as tTools
from scriptTools.charLength import charlen, longercharlen


#招聘信息表
class JobInfo(models.Model):
  job_id = models.AutoField(primary_key=True, auto_created=True)
  job_name = models.CharField(default="", blank=True, max_length=charlen)
  job_category = models.CharField(default="", blank=True, max_length=charlen)
  min_education = models.CharField(default="", blank=True, max_length=charlen)
  min_salary = models.IntegerField(default=0)
  max_salary = models.IntegerField(default=0)
  job_describe = models.CharField(default="", blank=True, max_length=longercharlen)
  company_name = models.CharField(default="", blank=True, max_length=charlen)
  job_demand = models.CharField(default="", blank=True, max_length=longercharlen)
  company_tele = models.CharField(default="", blank=True, max_length=charlen)
  company_email = models.CharField(default="", blank=True, max_length=charlen)
  company_contact_name = models.CharField(default="", blank=True, max_length=charlen)
  job_uuid = models.CharField(default="", blank=True, max_length=charlen)
  job_create_time = models.CharField(default=tTools.dateStdTime, max_length=charlen, blank=True)
  job_end_time = models.CharField(default="", blank=True, max_length=charlen)
  job_status = models.CharField(default="进行中", blank=True, max_length=charlen)
