from django.shortcuts import render
from django.core.paginator import Paginator
import scriptTools.mydecorator as mydecorator
import scriptTools.timeTools as timeTools
import scriptTools.myZip as myZip
import scriptTools.fieldsMap as fieldsMap
from django.core import serializers
from django.utils.encoding import escape_uri_path

import json
import uuid

from jobApp.models import JobInfo
from userApp.models import UserInfo, UserJobInfo, ResumeInfo
from adminApp.models import AdminInfo

from django.http import FileResponse
import os
import shutil
from zipfile import ZipFile


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


# http://127.0.0.1:8000/api/adminApp/outputAllResumeInfo/
def outputAllResumeInfo(request):
  nowDirPath = os.path.abspath(os.path.dirname(__file__))
  storeDirPath = os.path.join(nowDirPath, "../../storeFiles")
  download_dir_name = "../downloadFiles/allResume"

  filename = "招聘汇总_{}.zip".format(timeTools.dateStdTime().replace(":", "_").replace("-", "_"))
  csvfilename = "招聘汇总表_{}.csv".format(timeTools.dateStdTime().replace(":", "_").replace("-", "_"))
  downloadDirPath = os.path.join(nowDirPath, download_dir_name)
  downloadFilePath = os.path.join(nowDirPath, "{}/{}".format(download_dir_name, filename))
  csv_file_path = os.path.join(nowDirPath, "{}/{}".format(download_dir_name, csvfilename))

  def zipAllResumeFile():
    if os.path.exists(downloadDirPath):
      shutil.rmtree(downloadDirPath)
    os.makedirs(downloadDirPath)

    def fileNameMap(src_name):
      src_name = str(src_name).replace("headimg\\", "")
      src_name = str(src_name).replace("resumefile", "")
      name_lists = str(src_name).split('\\')
      try:
        if len(name_lists) > 1:
          user_uuid = name_lists[1]
          resume_name = ResumeInfo.objects.get(user_uuid=user_uuid).resume_name
          src_name = str(src_name).replace(user_uuid, resume_name + user_uuid[:8])
      except Exception as e:
        print("异常", str(e))

      # \964146c60b9311ebb0b38030491cc416\headimg\qq_pic_merged_1599735938126.jpg
      # \964146c60b9311ebb0b38030491cc416\resumefile\成绩单.pdf
      return src_name

    myZip.zip_dir(storeDirPath, downloadFilePath, fileNameMap)

  def productAllResumeCsv():
    res_str = ""
    # [{'user_job_id': 1, 'user_uuid': '964146c60b9311ebb0b38030491cc416', 'job_uuid': 'f748bf8a0ba211ebb2368030491cc416', 'deliver_status': '申请中'}]
    res_list = []
    query_index = 0
    for one_record in UserJobInfo.objects.all().values():
      user_uuid = one_record["user_uuid"]
      job_uuid = one_record["job_uuid"]
      user_info = ResumeInfo.objects.all().filter(user_uuid=user_uuid).values()[0]
      job_info = JobInfo.objects.all().filter(job_uuid=job_uuid).values()[0]
      if query_index == 0:
        fields = list(user_info.keys()) + list(job_info.keys())
        fields = [str(i).replace(",", "，") for i in fields]
        res_list.append([fieldsMap.get_chinese_name(i) for i in fields])
      fields_value = list(user_info.values()) + list(job_info.values())
      fields_value = ['"{}"'.format(str(i).replace(",", "，").replace('"', '`')) for i in fields_value]
      res_list.append(fields_value)
      query_index += 1
    res_str = "\n".join([",".join(y) for y in res_list])
    with open(csv_file_path, "w", encoding="utf8") as f:
      f.write(res_str)
    with ZipFile(downloadFilePath, "a") as myzip:
      myzip.write(csv_file_path, csvfilename)

  # filename = "招聘汇总表-日期时间.csv"
  zipAllResumeFile()
  productAllResumeCsv()
  response = FileResponse(open(downloadFilePath, 'rb'))
  response['Content-Type'] = 'application/octet-stream'
  response['Content-Disposition'] = 'attachment;filename="{}"'.format(escape_uri_path(filename))
  return response
