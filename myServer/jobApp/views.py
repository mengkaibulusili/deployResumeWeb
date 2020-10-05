from django.shortcuts import render
import scriptTools.mydecorator as mydecorator
import json
import uuid
from jobApp.models import JobInfo
from django.core import serializers
from django.core.paginator import Paginator
from django.db import transaction


@mydecorator.httpTry
def usefucbyname(request, fucname):
  return eval(fucname)(request)


# 管理员发布的招聘信息,publish实际上就是将前端传回来的信息写入数据库


@mydecorator.httpData
def hello(request):
  return "hello kiki !"


# 测试数据 http://127.0.0.1:8000/api/jobApp/publishJobInfo/?data={"job_name":"前端工程师","job_category":"互联网/程序开发","min_education":"大学本科","min_salary":"5000","max_salary":"12000","job_describe":"熟悉Vue/React等热门前端框架,有相关工作经验者优先录取","company_name":"环球企业中国市场研究院","job_demand":"有上进心对工作有强烈的责任感，有问题到我而止的精神","company_tele":"123456789","company_email":"XXXX@XXX.com","job_end_time":"2021年3月21日"}
# 管理员发布的招聘信息,publish实际上就是将前端传回来的信息写入数据库
@mydecorator.httpRes
def publishJobInfo(request):
  data_dict = json.loads(request.GET.get("data"))
  data_dict["job_uuid"] = str(uuid.uuid1()).replace("-", "")
  JobInfo(**data_dict).save()  # 将前端传回来的额字典解包写入数据库


#http://127.0.0.1:8000/api/jobApp/selectJobInfo
# 招聘信息的查询:查询全部的招聘信息


@mydecorator.httpData
def selectJobInfo(request):
  all_jobs = JobInfo.objects.all()
  #因为不确定数据库中会有多少条数据，所以先查一下有多少条数据
  num = JobInfo.objects.count()
  #获取JobInfo表中所有的招聘信息
  if (num):
    return json.loads(serializers.serialize("json", all_jobs))
  else:
    raise Exception("db is null!")


@mydecorator.httpData
def selectJobById(request):
  data_dict = json.loads(request.GET.get("data"))
  job_id = data_dict["job_id"]
  return json.loads(serializers.serialize("json", JobInfo.objects.filter(job_id=job_id)))


#测试 http://127.0.0.1:8000/api/jobApp/selectJobInfoByOptions/?data={"page_index":"1","max_salary":"15000","min_salary":"4999","min_education":"大学本科","job_category":"互联网/程序开发","job_name":"前端工程师","job_create_time": "20200927"}
# 按照发布时间job_create_time ,职位名称job_name，行业类别job_category , 最低学历公司名称min_education,  >= 最低薪水min_salary , <=最高薪水max_salary 进行搜索
@mydecorator.httpData
def selectJobInfoByOptions(request):
  data_dict = json.loads(request.GET.get("data"))
  page_index = int(data_dict["page_index"])
  # print(page_index)
  # print("page_index的类型是", type(page_index))
  d_ = data_dict
  for key_name in ["job_create_time", "job_name", "job_category", "min_education", "job_status"]:
    d_[key_name] = d_[key_name] if d_.__contains__(key_name) else ""
  d_["min_salary"] = int(d_["min_salary"]) if d_.__contains__("min_salary") else 0
  d_["max_salary"] = int(d_["max_salary"]) if d_.__contains__("max_salary") else 99999999999
  # for i in data_dict:
  #   print(data_dict[i])
  all_jobs = JobInfo.objects.filter(
    job_create_time__contains=d_["job_create_time"],
    job_name__contains=d_["job_name"],
    job_category__contains=d_["job_category"],
    min_education__contains=d_["min_education"],
    job_status__contains=d_["job_status"],
    min_salary__gte=int(d_["min_salary"]),
    max_salary__lte=int(d_["max_salary"]),
  ).order_by("-job_create_time")
  #每页的人数
  eachcount = 10
  paginator = Paginator(all_jobs, eachcount)
  #获取传入页码的当前页的要显示的所有人
  all_jobs = paginator.page(page_index)
  #返回序列化的当前页所用用户的数据
  return {"lists": json.loads(serializers.serialize("json", all_jobs)), "sum_page": paginator.num_pages}


#测试http://127.0.0.1:8000/api/jobApp/setJobStatus/?data={"job_uuid":"f79df13a006711eb9a30d66a6a55781d","job_status": "已结束"}
#修改jobInfo的状态
@mydecorator.httpRes
def setJobStatus(request):
  data_dict = json.loads(request.GET.get("data"))
  job_uuid = data_dict["job_uuid"]
  job_status = data_dict["job_status"]
  with transaction.atomic():
    job = JobInfo.objects.get(job_uuid=data_dict["job_uuid"])
    job.job_status = data_dict["job_status"]
    job.save()
