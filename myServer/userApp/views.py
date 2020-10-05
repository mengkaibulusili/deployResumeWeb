from django.core import serializers
from django.shortcuts import render
import scriptTools.mydecorator as mydecorator
import json
import uuid
# Create your views here.
from userApp.models import UserInfo, UserJobInfo, ResumeInfo
from jobApp.models import JobInfo
from scriptTools.dealCsv import dealCsvFile
from django.core import serializers
from django.core.paginator import Paginator
from scriptTools.dealUploadFiles import dealUploadFile, dealResumeDir, getResumeFileNameByUuid

from django.db import transaction


@mydecorator.httpTry
def usefucbyname(request, fucname):
  return eval(fucname)(request)


@mydecorator.httpData
def hello(request):
  return "hello kiki !"


@mydecorator.httpData
def register(request):
  data_dict = json.loads(request.GET.get("data"))
  data_dict["user_uuid"] = str(uuid.uuid1()).replace("-", "")
  with transaction.atomic():
    UserInfo(**data_dict).save()  # 将字典解包存入数据库中
  return data_dict


@mydecorator.httpData
def login(request):
  # 获取前面传回来的数据
  data_dict = json.loads(request.GET.get("data"))

  if (UserInfo.objects.filter(user_tele=data_dict["user_tele"])):
    # 判断为真说明数据库中存在这个手机号
    if (UserInfo.objects.filter(user_tele=data_dict["user_tele"]).filter(user_pwd=data_dict["user_pwd"])):
      # 这里在前端应该显示一个登录成功的提示,我在这里给前端返回一个表示查询成功的状态码，比如00
      data_dict["user_uuid"] = UserInfo.objects.get(user_tele=data_dict["user_tele"]).user_uuid
      return data_dict
    else:
      # 这里可能出现密码出错的情况，给前端返回一个密码出错的状态码，比如11
      raise Exception("Wrong Pwd")
  else:
    # 这个情况是不存该手机号，请用户先进行注册，再登录,这里返回一个状态码，或者返回到注册页面
    raise Exception("Don't exist")


@mydecorator.httpRes
def uploadresume(request):
  data_dict = json.loads(request.GET.get("data"))
  data_dict["resume_uuid"] = str(uuid.uuid1()).replace("-", "")
  select_res = ResumeInfo.objects.filter(user_uuid=data_dict["user_uuid"])
  if select_res:
    with transaction.atomic():
      select_res[0].delete()
      ResumeInfo(**data_dict).save()  # 将字典解包存入数据库中
  else:
    ResumeInfo(**data_dict).save()
    # raise (Exception("不存在这个用户"))


# http://localhost:8000/api/userApp/getUserInfoByUuid/?data={"user_uuid":"null"}
@mydecorator.httpData
def getUserInfoByUuid(request):
  data_dict = json.loads(request.GET.get("data"))
  return json.loads(serializers.serialize("json", ResumeInfo.objects.filter(user_uuid=data_dict["user_uuid"])))


# http://localhost:8000/api/userApp/getResumeFileName/?data={"user_uuid":"null"}
@mydecorator.httpData
def getResumeFileName(request):
  data_dict = json.loads(request.GET.get("data"))
  return {"resume_file_name": getResumeFileNameByUuid(data_dict["user_uuid"])}


# http://localhost:8000/api/userApp/deliverJob/?data={"user_uuid":"null","job_uuid":"12122"}
@mydecorator.httpRes
def deliverJob(request):
  data_dict = json.loads(request.GET.get("data"))
  UserJobInfo(**data_dict).save()


# http://localhost:8000/api/userApp/getDeliverStatus/?data={"user_uuid":"null","job_uuid":"12122"}
@mydecorator.httpData
def getDeliverStatus(request):
  data_dict = json.loads(request.GET.get("data"))
  select_res = UserJobInfo.objects.filter(
    user_uuid=data_dict["user_uuid"],
    job_uuid=data_dict["job_uuid"],
  )
  if select_res:
    return {"deliver_status": select_res[0].deliver_status}
  return {"deliver_status": "未投递"}


# http://localhost:8000/api/userApp/setDeliverStatus/?data={"user_uuid":"null","job_uuid":"12122","deliver_status":"通过"}
@mydecorator.httpRes
def setDeliverStatus(request):
  data_dict = json.loads(request.GET.get("data"))
  job_id = data_dict["job_id"]
  job_uuid = JobInfo.objects.get(job_id=job_id).job_uuid
  select_res = UserJobInfo.objects.filter(
    user_uuid=data_dict["user_uuid"],
    job_uuid=job_uuid,
  )
  if select_res:
    select_res[0].deliver_status = data_dict["deliver_status"]
    select_res[0].save()
  else:
    raise (Exception("have not this deliver record!"))


@mydecorator.httpRes
def uploadResumeFile(request):
  # <QueryDict: {'modelname': ['a'], 'filesize': ['218 B']}>
  sFile = request.FILES.get('file')
  postDict = dict(request.POST)
  data = {x: postDict[x][0] for x in postDict.keys()}

  resume_file_name = data["resume_file_name"] if data.__contains__("resume_file_name") else ""
  if resume_file_name != "":
    dealResumeDir(data["user_uuid"])
    dealUploadFile(data["user_uuid"], resume_file_name, sFile)
  else:
    raise (Exception("upload fail"))


@mydecorator.httpData
def showresume(request):
  data_dict = json.loads(request.GET.get("data"))
  all_resume = serializers.serialize("json", ResumeInfo.objects.filter(user_uuid=data_dict["user_uuid"]).all())
  # 因为不确定数据库中会有多少条数据，所以先查一下有多少条数据
  num = ResumeInfo.objects.count()
  # 获取JobInfo表中所有的招聘信息
  if (num):
    return all_resume
  else:
    raise Exception("db is null!")


# @mydecorator.httpRes
# def deleresume(request):
#   # 需要添加一行获取已登录账号手机的代码
#   data_dict = json.loads(request.GET.get("data"))
#   ResumeInfo.objects.filter(resume_tele=data_dict["user_tele"]).delete()


@mydecorator.httpData
def showmydelivered(request):
  pass

  # #接受文件模块
  # @mydecorator.httpRes
  # def putCustomJob(request):
  #   # <QueryDict: {'modelname': ['a'], 'filesize': ['218 B']}>
  #   sFile = request.FILES.get('file')
  #   postDict = dict(request.POST)
  #   data = {x: postDict[x][0] for x in postDict.keys()}
  #   uid = str(uuid.uuid1()).replace("-", "")
  #   data["jobuuid"] = uid

  #   csvName = data["csvname"] if data.__contains__("csvname") else ""
  #   if not csvName.endswith(".csv"):
  #     raise Exception("file must end with csv")
  #   if csvName != "":
  #     data["savedir"] = dealCsvFile(uid, "input.csv", sFile)

  #   # 投递任务 ，如果投递失败 抛出 异常 之后的代码不会执行
  #   shareQ.q.put_nowait(data)

  #   # the JSON object must be str, bytes or bytearray, not NoneType
  #   JobInfo(**data).save()


#先测试一下返回的是什么类型的数据 http://127.0.0.1:8000/api/userApp/getAllUser/?data={"page_index": "1","user_tele":"1823112"}
#查询所有的用户，带着分页器，（不需要查询用户的密码）
#返回的查询结果是这样的<QuerySet [{'user_id': 1, 'user_tele': '1823112', 'user_email': 'kiki@qq.com', 'create_time': '20200926-15:54:02'}, {'user_id': 2, 'user_tele': '11111111111', 'user_email': '@qq.com', 'create_time': '20200926-16:02:03'}, {'user_id': 3, 'user_tele': '11111111112', 'user_email': '@qq.com', 'create_time': '20200926-16:06:12'}]>
@mydecorator.httpData
def getAllUser(request):
  #根据前端传回来的data获取页码
  data_dict = json.loads(request.GET.get("data"))
  page_index = data_dict["page_index"]
  d_ = data_dict
  for key_name in ["user_tele", "user_email", "create_time"]:
    d_[key_name] = d_[key_name] if d_.__contains__(key_name) else ""
  allusers = UserInfo.objects.defer("user_pwd").filter(user_tele__contains=d_["user_tele"], user_email__contains=d_["user_email"], create_time__contains=d_["create_time"]).order_by("-create_time")
  #每页的人数
  eachcount = 10
  paginator = Paginator(allusers, eachcount)
  #获取传入页码的当前页的要显示的所有人
  allusers = paginator.page(page_index)
  #返回序列化的当前页所用用户的数据
  return {"lists": json.loads(serializers.serialize("json", allusers)), "sum_page": paginator.num_pages}
