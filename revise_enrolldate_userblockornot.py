from google.cloud import firestore
import json
import datetime

# 因為雲端大師資料庫欄位型別沒有統整好，透過此 py，將資料庫所有用戶的
# line_user_is_blocked 都統一為 boolean
# line_user_enroll_date 都統一為 int

# 先備份資料庫在執行，避免資料全不見或異常

def revise_enrolldate_userblockornot():
    db = firestore.Client()
    users_ref = db.collection("CloudMasterLineBotUser")
    docs = users_ref.stream()
    i = 0
    for doc in docs:
        line_user_id = doc.id
        user_stat_dict = doc.to_dict()

        # 先將檔案保存，避免等等出錯，資料全不見
        with open("_backUp_CloudMasterLineBotUser_2022-11.json", 'a', encoding="utf-8") as fout:
            json.dump(user_stat_dict, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")

        if user_stat_dict["line_user_is_blocked"] == "false":
            user_stat_dict["line_user_is_blocked"] = False
        elif user_stat_dict["line_user_is_blocked"] == "true":
            user_stat_dict["line_user_is_blocked"] == True
        
        try:
            user_stat_dict["line_user_enroll_date"] = user_stat_dict["line_user_enroll_date"].timestamp_pb().seconds
        except:
            if type(user_stat_dict["line_user_enroll_date"]) == float:
                user_stat_dict["line_user_enroll_date"] = int(user_stat_dict["line_user_enroll_date"])
                
            elif type(user_stat_dict["line_user_enroll_date"]) == str:
                format_date = datetime.datetime.strptime(user_stat_dict["line_user_enroll_date"], '%Y-%m-%d %H:%M:%S.%f%z')
                user_stat_dict["line_user_enroll_date"] = int(format_date.timestamp())

        # set 檔案
        db.collection("CloudMasterLineBotUser").document(line_user_id).set(user_stat_dict)

        # 算次數
        i += 1
        print(i)

revise_enrolldate_userblockornot()