from zipfile import ZipFile
import os


def get_all_abs_file(src_dir_path):
  files_path = []
  for x, y, z in os.walk(src_dir_path):
    files_path += [os.path.join(x, i) for i in z]
    # print(x, " ***** ", y, " *** ", [os.path.join(x, i) for i in z])
  return files_path


def zip_dir(src_dir_path, des_path, fileNameMap=None):
  files_abs_path = get_all_abs_file(src_dir_path)
  # print(files_abs_path)
  des_path = os.path.abspath(des_path)
  with ZipFile(des_path, "w") as myzip:
    for one_file_path in files_abs_path:
      if fileNameMap == None:
        myzip.write(one_file_path, one_file_path.replace(src_dir_path, ""))
      else:
        myzip.write(one_file_path, fileNameMap(one_file_path.replace(src_dir_path, "")))