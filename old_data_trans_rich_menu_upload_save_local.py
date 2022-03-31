from google.cloud import firestore

import pandas as pd
import json


# 使用前，請先更改 
# 金鑰、專案id、讀取json的路徑、寫入csv的路徑

list_ = []

# db = firestore.Client()
db = firestore.Client.from_service_account_json("./cloud-master-3-29-cfb7e9371055.json", project='cloud-master-3-29')

with open('ccs_line_richmenus.json', 'r', encoding='utf-8') as file:
    for line in file:
        line = json.loads(line)
        # 變更鍵的名稱
        # line[k_new] = line.pop(k_old)
        line['rich_menu_name'] = line.pop('line_richmenu_custom_name')
        line['rich_menu_pic_url'] = line.pop('line_richmenu_pic_url')
        line['rich_menu_config'] = line.pop('line_richmenu_config')
        line['custom_description'] = line.pop('line_richmenu_custom_description')
        line['rich_menu_id'] = line.pop('line_richmenu_id')
        line['custom_name'] = line['rich_menu_name']
        del line['line_channel_id']

        with open("CloudMasterLineBotRichMenu.json", 'a', encoding="utf-8") as fout:
            json.dump(line, fout, ensure_ascii=False, sort_keys=True, default=str)
            fout.write("\n")

        db.collection(u'CloudMasterLineBotRichMenu').document(line['rich_menu_name']).set(line)

        list_.append(line)
df = pd.json_normalize(list_)

df.to_csv("CloudMasterLineBotRichMenu.csv")
