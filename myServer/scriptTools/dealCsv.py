import os

# No such file or directory: 'C:\\gitproj\\autotrain\\myServer\\storeFiles\\ccc1104cefe311ea8a380871908061a4\\新建文本文档.txt'


def dealCsvFile(uid, fn, fd):
  pdir = os.path.dirname
  pjoin = os.path.join
  myFile = fd
  if myFile:
    savedir = pjoin(pdir(pdir(__file__)), 'storeFiles')
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
