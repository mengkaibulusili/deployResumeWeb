import os

# No such file or directory: 'C:\\gitproj\\autotrain\\myServer\\storeFiles\\ccc1104cefe311ea8a380871908061a4\\新建文本文档.txt'
import shutil


def getResumeFileNameByUuid(uid):
  pdir1 = os.path.abspath
  pdir = os.path.dirname
  pjoin = os.path.join
  savedir = pjoin(pdir(pdir(pdir(pdir1(__file__)))), 'storeFiles')
  if not os.path.exists(savedir):
    os.mkdir(savedir)
  savedir = pjoin(savedir, str(uid))
  if os.path.exists(savedir):
    # 默认只有 一份简历文件
    return os.listdir(savedir)[0] if len(os.listdir(savedir)) > 0 else "未提交"
  return "未提交"


def dealResumeDir(uid):
  pdir1 = os.path.abspath
  pdir = os.path.dirname
  pjoin = os.path.join
  savedir = pjoin(pdir(pdir(pdir(pdir1(__file__)))), 'storeFiles')
  if not os.path.exists(savedir):
    os.mkdir(savedir)
  savedir = pjoin(savedir, str(uid))
  if os.path.exists(savedir):
    shutil.rmtree(savedir)


def dealUploadFile(uid, fn, fd):
  pdir1 = os.path.abspath
  pdir = os.path.dirname
  pjoin = os.path.join
  myFile = fd
  if myFile:
    savedir = pjoin(pdir(pdir(pdir(pdir1(__file__)))), 'storeFiles')
    if not os.path.exists(savedir):
      os.mkdir(savedir)
    savedir = pjoin(savedir, str(uid))
    if not os.path.exists(savedir):
      os.mkdir(savedir)
    destination = open(pjoin(savedir, fn), 'wb+')
    for chunk in myFile.chunks():
      destination.write(chunk)
    destination.close()
    return savedir
  return ""
