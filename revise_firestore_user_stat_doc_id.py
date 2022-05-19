from google.cloud import firestore
import json

# 提醒  先 save 再做，避免資料全部不見

def revise_firestore_user_stat_doc_id(user_stat_table_name):
    # 獲得資料集的所有文件內容
    # db = firestore.Client()
    db = firestore.Client.from_service_account_json("cloud-master-test0426-f3036b7d84cb.json", project='cloud-master-test0426')
 
    # 連接 userStat 資料集
    users_ref = db.collection(user_stat_table_name)  # CloudMasterExamQuestionAwsSaaUserStat 資料集
    docs = users_ref.stream()
    i = 0
    # 迴圈每一個檔案
    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()}')
        # break
        line_user_id = doc.id
        user_stat_dict = doc.to_dict()
        
        # 先將檔案保存，避免等等出錯，資料全不見
        with open("_backup2_" + user_stat_table_name +".json", 'a', encoding="utf-8") as fout:
            json.dump(user_stat_dict, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")

        # set 檔案
        db.collection(user_stat_table_name).document(user_stat_dict["user_id"]).set(user_stat_dict)

        # 刪除原本的檔案
        delete_ref = db.collection(user_stat_table_name).document(line_user_id)  
        delete_ref.delete()

        # 算次數
        i += 1
        print(i)

revise_firestore_user_stat_doc_id(user_stat_table_name = "CloudMasterExamQuestionAwsSoaUserStat")