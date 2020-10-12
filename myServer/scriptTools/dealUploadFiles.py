import os

# No such file or directory: 'C:\\gitproj\\autotrain\\myServer\\storeFiles\\ccc1104cefe311ea8a380871908061a4\\新建文本文档.txt'
import shutil

resumedir = "resumefile"

headimgdir = "headimg"


def getFileByUuidAndtype(uid, typedir):
  pdir1 = os.path.abspath
  pdir = os.path.dirname
  pjoin = os.path.join
  savedir = pjoin(pdir(pdir(pdir(pdir1(__file__)))), 'storeFiles')
  if not os.path.exists(savedir):
    os.mkdir(savedir)
  savedir = pjoin(savedir, str(uid))
  savedir = pjoin(savedir, typedir)
  if os.path.exists(savedir):
    # 默认只有 一份简历文件
    return os.listdir(savedir)[0] if len(os.listdir(savedir)) > 0 else "未提交"
  return "未提交"


def getResumeFileNameByUuid(uid):
  return getFileByUuidAndtype(uid, resumedir)


def getHeadimgNameByUuid(uid):
  return getFileByUuidAndtype(uid, headimgdir)


def dealSaveDir(uid, typedir):
  pdir1 = os.path.abspath
  pdir = os.path.dirname
  pjoin = os.path.join
  savedir = pjoin(pdir(pdir(pdir(pdir1(__file__)))), 'storeFiles')
  if not os.path.exists(savedir):
    os.mkdir(savedir)
  savedir = pjoin(savedir, str(uid))
  if not os.path.exists(savedir):
    os.mkdir(savedir)
  savedir = pjoin(savedir, typedir)
  if os.path.exists(savedir):
    shutil.rmtree(savedir)


def dealResumeDir(uid):
  dealSaveDir(uid, resumedir)


def dealHeadImgDir(uid):
  dealSaveDir(uid, headimgdir)


def saveFile(uid, fn, fd, typedir):
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
    savedir = pjoin(savedir, typedir)
    if not os.path.exists(savedir):
      os.mkdir(savedir)
    destination = open(pjoin(savedir, fn), 'wb+')
    for chunk in myFile.chunks():
      destination.write(chunk)
    destination.close()
    return savedir
  return ""


def dealUploadFile(uid, fn, fd):
  return saveFile(uid, fn, fd, resumedir)


def dealUploadHeadImg(uid, fn, fd):
  return saveFile(uid, fn, fd, headimgdir)
