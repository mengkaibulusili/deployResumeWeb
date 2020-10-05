import shutil
import os


def tryRm(f):
  def x(*args, **kwargs):
    try:
      f(*args, **kwargs)
    except Exception as e:
      print(str(e))

  return x


@tryRm
def rmFiles(needRmFiles):
  for file in needRmFiles:
    os.remove(file)
    print("rm file", file)


@tryRm
def rmDirs(needRmDirs):
  for dir in needRmDirs:
    shutil.rmtree(dir)
    print("rm dir ", dir)


def cleanCache():
  dirRoot = os.path.dirname(__file__)

  dirName = "__pycache__"
  fileList = ["db.sqlite3", "_initial.py", "_auto_"]
  needRmDirs = []
  needRmFiles = []
  for root, dirs, files in os.walk(dirRoot):
    for dir in dirs:
      if (dir.find(dirName) != -1):
        dirPath = os.path.join(root, dir)
        needRmDirs.append(dirPath)

    for onefile in files:
      for rmName in fileList:
        if (onefile.find(rmName) != -1):
          filePath = os.path.join(root, onefile)
          needRmFiles.append(filePath)

  rmDirs(needRmDirs)
  rmFiles(needRmFiles)


def newDB():
  dirRoot = os.path.dirname(__file__)
  execManageFile = os.path.join(dirRoot, "manage.py")
  os.system("python {} makemigrations".format(execManageFile))
  os.system("python {} migrate".format(execManageFile))


def reNewDB():
  cleanCache()
  newDB()


if __name__ == "__main__":
  reNewDB()