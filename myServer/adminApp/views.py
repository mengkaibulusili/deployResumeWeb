from django.shortcuts import render
from django.core.paginator import Paginator
import scriptTools.mydecorator as mydecorator
from django.core import serializers

import json
import uuid

from jobApp.models import JobInfo
from userApp.models import UserInfo, UserJobInfo, ResumeInfo
from adminApp.models import AdminInfo


@mydecorator.httpTry
def usefucbyname(request, fucname):
  return eval(fucname)(request)


#测试
@mydecorator.httpData
def hello(request):
  return "hello kiki !"


# @mydecorator.httpRes
# def register(request):
#   data_dict = json.loads(request.GET.get("data"))
#   data_dict["admin_uuid"] = str(uuid.uuid1()).replace("-", "")
#   AdminInfo(**data_dict).save()  #将字典解包存入数据库中


#http://127.0.0.1:8000/api/adminApp/adminLogin/?data={"admin_tele": "admin","admin_pwd":"123456"}
#验证管理员的登录
@mydecorator.httpData
def adminLogin(request):
  data_dict = json.loads(request.GET.get("data"))
  if (AdminInfo.objects.filter(admin_tele=data_dict["admin_tele"])):
    # 判断是否存在这个管理员
    if (AdminInfo.objects.filter(admin_tele=data_dict["admin_tele"]).filter(admin_pwd=data_dict["admin_pwd"])):
      pass
    else:
      raise Exception("Wrong Pwd")
  else:
    raise Exception("Not Exist")
  return data_dict


# #http://127.0.0.1:8000/api/adminApp/getCandidateInfo/?data={"query_job_id": "1","page_index":"1"}
@mydecorator.httpData
def getCandidateInfo(request):
  data_dict = json.loads(request.GET.get("data"))
  page_index = int(data_dict["page_index"])
  job_id = data_dict["query_job_id"]
  deliver_status = data_dict["deliver_status"]
  all_delivers = []
  if job_id != "":
    query_res = JobInfo.objects.filter(job_id=job_id)
    if query_res:
      job_uuid = query_res[0].job_uuid
      all_delivers = UserJobInfo.objects.filter(job_uuid=job_uuid, deliver_status__contains=deliver_status)

  else:
    all_delivers = UserJobInfo.objects.filter(deliver_status__contains=deliver_status)
  all_user_uuid = [x.user_uuid for x in all_delivers]
  all_candidates = ResumeInfo.objects.filter(user_uuid__in=all_user_uuid)

  eachcount = 10
  paginator = Paginator(all_candidates, eachcount)
  #获取传入页码的当前页的要显示的所有人
  candidates = paginator.page(page_index)
  #返回序列化的当前页所用用户的数据
  return {"lists": json.loads(serializers.serialize("json", candidates)), "sum_page": paginator.num_pages}