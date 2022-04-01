from google.cloud import firestore

import pandas as pd
import json
import uuid


line_bot_users = []
users = []

# 成就紀錄
saa_stat = []
soa_stat = []


# db = firestore.Client()
# 金鑰、專案id
db = firestore.Client.from_service_account_json("./cloud-master-3-29-cfb7e9371055.json", project='cloud-master-3-29')

# 讀取的路徑
with open('test0401.json', 'r', encoding='utf-8') as file:
    # 舊客戶迴圈
    for line in file:
        saa_user_stat = {}
        soa_user_stat = {}
        line_bot_user_dict = {}
        user_dict = {}  
        # 取出舊客戶字典
        line = json.loads(line)
        print(line['line_user_nickname'])
        # line-bot-user_dict
        line_bot_user_dict['user_id'] = str(uuid.uuid4())
        line_bot_user_dict['line_user_id'] = line['line_user_id']
        line_bot_user_dict['line_channel_id'] = line['line_channel_id']
        line_bot_user_dict['line_user_nick_name'] = line['line_user_nickname']
        line_bot_user_dict['line_user_status'] = line['line_user_status']
        line_bot_user_dict['line_user_pic_url'] = line['line_user_pic_url']
        line_bot_user_dict['line_default_language'] = line['line_user_system_language']
        line_bot_user_dict['line_user_is_blocked'] = line['line_user_is_blocked']
        line_bot_user_dict['line_user_enroll_date'] = line['line_user_enroll_date']
        line_bot_user_dict['line_rich_menu_link_custom_name'] = line['line_richmenu_link_custom_name']
        line_bot_user_dict['line_user_email'] = ''
        line_bot_user_dict['line_user_other_info'] = line['line_user_other_info']
        line_bot_user_dict['user_system_language'] = line['aws_saa_certificate_history']['ccs_language']

        # user_dict
        user_dict['user_id'] = line_bot_user_dict['user_id']
        user_dict['user_email'] = ''
        user_dict['user_point'] = int(line['aws_saa_certificate_history']['payment_question_quota']) + int(line['aws_sysops_certificate_history']['payment_question_quota'])
        user_dict['user_name'] = line['line_user_nickname']
        user_dict['user_age'] = 999
        user_dict['user_sex'] = ''
        user_dict['user_job_title'] = ''
        user_dict['user_phone_number'] = ''

        # 成就紀錄
        saa_user_stat['user_id'] = line_bot_user_dict['user_id']
        saa_user_stat['line_user_id'] = line['line_user_id']
        saa_user_stat['user_email'] = ' '
        saa_user_stat['total_answer_amount'] = line['aws_saa_certificate_history']['total_answer_amount']
        saa_user_stat['true_amount'] = line['aws_saa_certificate_history']['true_answer_amount']

        soa_user_stat['user_id'] = line_bot_user_dict['user_id']
        soa_user_stat['line_user_id'] = line['line_user_id']
        soa_user_stat['user_email'] = ' '
        soa_user_stat['total_answer_amount'] = line['aws_sysops_certificate_history']['total_answer_amount']
        soa_user_stat['true_amount'] = line['aws_sysops_certificate_history']['true_answer_amount']

        line_bot_users.append(line_bot_user_dict)
        print(line_bot_users)
        users.append(user_dict)

        # 成就
        saa_stat.append(saa_user_stat)
        soa_stat.append(soa_user_stat)

# 寫入 json 路徑
        with open("CloudMasterLineBotUser.json", 'a', encoding="utf-8") as fout:
            json.dump(line_bot_user_dict, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")

        with open("CloudMasterUser.json", 'a', encoding="utf-8") as fout:
            json.dump(user_dict, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")

        # 成就
        with open("ExamQuestionAwsSaaUserStat.json", 'a', encoding="utf-8") as fout:
            json.dump(saa_user_stat, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")
        with open("ExamQuestionAwsSoaUserStat.json", 'a', encoding="utf-8") as fout:
            json.dump(soa_user_stat, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")

        db.collection(u'CloudMasterLineBotUser').document(line_bot_user_dict['line_user_id']).set(line_bot_user_dict)
        
        db.collection(u'CloudMasterUser').document(user_dict['user_id']).set(user_dict)

        # 成就
        db.collection(u'ExamQuestionAwsSaaUserStat').document(line_bot_user_dict['line_user_id']).set(saa_user_stat)
        db.collection(u'ExamQuestionAwsSoaUserStat').document(line_bot_user_dict['line_user_id']).set(soa_user_stat)

        
    # csv 路徑
    line_bot_users_df = pd.json_normalize(line_bot_users)
    line_bot_users_df.to_csv("CloudMasterLineBotUser.csv")

    users_df = pd.json_normalize(users)
    users_df.to_csv("CloudMasterUser.csv")

    # 成就
    saa_user_stat_df = pd.json_normalize(saa_stat)
    saa_user_stat_df.to_csv("ExamQuestionAwsSaaUserStat.csv")

    soa_user_stat_df = pd.json_normalize(soa_stat)
    soa_user_stat_df.to_csv("ExamQuestionAwsSoaUserStat.csv")