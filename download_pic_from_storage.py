# 下載 bucket 內每個用戶的照片，將這些照片整理成第三代要的目錄，並且更改照片名稱為 user_img.png
# 第二代的目錄範例：
# cloud-certificate-bot-user-info/U8a07664bc0d08dd21456706a1bb8527a/user_pic.png

# 第三代的目錄範例：
# cloud-master-info-test0426/line-bot/users/Ufba156b698b0200348f0e8bbb8958534/user_img.png

# 使用前，請先更新或確認：是在第二代專案執行、第 53 行寫舊版放用戶照片的值區名字、確認 CloudMasterLineBotUser.json 存在

from google.cloud import storage
import os
import json

# 下載 object
def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    # 值區的目錄
    blob = bucket.blob(source_blob_name)
    # 本地目錄
    blob.download_to_filename(destination_file_name)

# 列出 object 
def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    storage_client = storage.Client()

    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)
    # print("Blobs:")
    for blob in blobs:
        if blob.name.endswith("user_pic.png"):
            return blob.name
        # print(blob.name)
        # return blobs.name
    # if delimiter:
        # print("Prefixes:")
        # for prefix in blobs.prefixes:
            # print(prefix)

# 得到所有的 line_user_id
def get_all_line_user_ids():
    line_user_ids_list = []
    with open('CloudMasterLineBotUser.json', 'r', encoding='utf-8') as file:

        for line in file:
            line = json.loads(line)
            line_user_ids_list.append(line['line_user_id'])
    return line_user_ids_list

"""邏輯：先從 CloudMasterLineBotUser.json 取出所有 line user id，
接著嘗試用列出物件的API，迴圈 line user id 看看有沒有照片；若有，將路徑存入清單，
將清單迴圈下載至本地"""

bucket_name = ""
line_user_ids_list = get_all_line_user_ids()
os.mkdir("line-bot")
os.mkdir("line-bot/users")

for line_user_id in line_user_ids_list:
    os.mkdir("line-bot/users/"+line_user_id)
    blob_path = list_blobs_with_prefix(bucket_name, line_user_id+"/")
    print(line_user_id)
    if blob_path:
        download_blob(bucket_name, blob_path, "line-bot/users/"+line_user_id+"/user_img.png")


