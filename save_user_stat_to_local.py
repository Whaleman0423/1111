from google.cloud import firestore
import json

def save_collection():
    # 獲得資料集的所有文件內容
    # db = firestore.Client()
    db = firestore.Client.from_service_account_json("cloud-master-test0426-f3036b7d84cb.json", project='cloud-master-test0426')
 
    # [START firestore_setup_dataset_read]
    # [START quickstart_get_collection]
    users_ref = db.collection(u'CloudMasterExamQuestionAwsSoaUserStat')  # CloudMasterExamQuestionAwsSaaUserStat 資料集
    docs = users_ref.stream()
    i = 0
    for doc in docs:
        # print(f'{doc.id} => {doc.to_dict()}')
        # break
        line_user_id = doc.id
        user_stat_dict = doc.to_dict()

        with open("_backup_CloudMasterExamQuestionAwsSoaUserStat.json", 'a', encoding="utf-8") as fout:
            json.dump(user_stat_dict, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")
        i += 1
        print(i)



save_collection()