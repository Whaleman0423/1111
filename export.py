# pip install google-cloud-firestore
from google.cloud import firestore

import json

 
def quickstart_get_collection():
    # 獲得資料集的所有文件內容
    # db = firestore.Client()
    db = firestore.Client.from_service_account_json("./cloud-master-3-29-cfb7e9371055.json", project='cloud-master-3-29')
 
    # [START firestore_setup_dataset_read]
    # [START quickstart_get_collection]
    users_ref = db.collection(u'CloudMasterLineBotUser')  # users 資料集
    docs = users_ref.stream()
 
    for doc in docs:
        with open("myoutput.json", 'a', encoding="utf-8") as fout:
            print(f'{doc.id} => {doc.to_dict()}')
    # [END quickstart_get_collection]
    # [END firestore_setup_dataset_read]
            json.dump(doc.to_dict(), fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")

quickstart_get_collection()