def get_chinese_name(column_english_name):
  english_name = "resume_id,user_uuid,resume_uuid,resume_school,resume_name,resume_tele,resume_email,resume_sex,resume_highest_degree,resume_location,resume_late_major,resume_expected_arrival_time,resume_graduation_date,resume_birthday,resume_skill,resume_award,resume_project_experience,resume_self_description,resume_internship,resume_job_intension,job_id,job_name,job_category,min_education,min_salary,max_salary,job_describe,company_name,job_demand,company_tele,company_email,job_uuid,job_create_time,job_end_time,job_status"
  chinese_name = "简历id,用户uuid,简历uuid,应聘者学校,应聘者姓名,应聘者电话,应聘者邮箱,应聘者性别,应聘者最高学历,应聘者所在地,应聘者专业,应聘者到岗时间,应聘者毕业时间,应聘者生日,应聘者能力,应聘者奖励,应聘者项目经验,应聘者自我介绍,应聘者实习经历,应聘者求职意向,岗位id,岗位名称,岗位类别,岗位最低学历,岗位最低薪水,岗位最高薪水,岗位描述,岗位公司名称,岗位能力要求,岗位联系电话,岗位邮箱,岗位uuid,岗位创建时间,岗位结束时间,岗位招聘状态"
  english_name = english_name.split(",")
  chinese_name = chinese_name.split(",")
  name_map = {}
  for index, value in enumerate(english_name):
    name_map[value] = chinese_name[index]
  if name_map.__contains__(column_english_name):
    return name_map[column_english_name]
  return "未知字段"