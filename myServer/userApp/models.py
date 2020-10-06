from django.db import models
import uuid
import scriptTools.timeTools as tTools
from scriptTools.charLength import charlen, longercharlen


# Create your models here.
class UserInfo(models.Model):
  user_id = models.AutoField(primary_key=True, auto_created=True)
  user_uuid = models.CharField(default="", blank=True, max_length=charlen)
  user_tele = models.CharField(unique=True, max_length=charlen)
  user_pwd = models.CharField(default="", blank=True, max_length=charlen)
  user_email = models.CharField(default="", blank=True, max_length=charlen)
  create_time = models.CharField(default=tTools.dateStdTime, max_length=charlen, blank=True)


class ResumeInfo(models.Model):
  resume_id = models.AutoField(primary_key=True, auto_created=True)
  user_uuid = models.CharField(default="", blank=True, max_length=charlen)
  resume_uuid = models.CharField(default="", blank=True, max_length=charlen)
  resume_school = models.CharField(default="", blank=True, max_length=charlen)
  resume_name = models.CharField(default="", blank=True, max_length=charlen)
  resume_tele = models.CharField(unique=True, max_length=charlen)
  resume_email = models.CharField(default="", blank=True, max_length=charlen)
  resume_sex = models.CharField(default="", blank=True, max_length=charlen)
  resume_highest_degree = models.CharField(default="", blank=True, max_length=charlen)
  resume_location = models.CharField(default="", blank=True, max_length=charlen)
  resume_late_major = models.CharField(default="", blank=True, max_length=charlen)

  resume_expected_arrival_time = models.CharField(default="", blank=True, max_length=charlen)
  resume_graduation_date = models.CharField(default="", blank=True, max_length=charlen)
  resume_birthday = models.CharField(default="", blank=True, max_length=charlen)

  resume_skill = models.CharField(default="", blank=True, max_length=longercharlen)
  resume_award = models.CharField(default="", blank=True, max_length=longercharlen)

  resume_project_experience = models.CharField(default="", blank=True, max_length=longercharlen)
  resume_self_description = models.CharField(default="", blank=True, max_length=longercharlen)
  resume_internship = models.CharField(default="", blank=True, max_length=longercharlen)
  resume_job_intension = models.CharField(default="", blank=True, max_length=longercharlen)


# 应聘者 和 招聘任务的关系表
class UserJobInfo(models.Model):
  user_job_id = models.AutoField(primary_key=True, auto_created=True)
  user_uuid = models.CharField(default="", blank=True, max_length=charlen)
  job_uuid = models.CharField(default="", blank=True, max_length=charlen)
  # 申请中 , 通过 , 淘汰
  deliver_status = models.CharField(default="申请中", blank=True, max_length=charlen)

  class Meta:
    # 联合约束   user_uuid  job_uuid 不能重复
    unique_together = ["user_uuid", "job_uuid"]


# class AdminInfo(models.Model):
#   admin_id = models.AutoField(primary_key=True, auto_created=True)
#   admin_uuid = models.CharField(default="", blank=True, max_length=charlen)
#   admin_tele = models.CharField(unique=True, max_length=charlen)
#   admin_pwd = models.CharField(default="", blank=True, max_length=charlen)
