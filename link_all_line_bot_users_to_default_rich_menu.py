from google.cloud import firestore
from linebot import LineBotApi
import json

db = firestore.Client()

# line-bot user
line_user_id_list_1 = []
line_user_id_list_2 = []
line_user_id_list_3 = []
line_user_id_list_4 = []
line_user_id_list_5 = []
i = 0
with open('CloudMasterLineBotUser.json', 'r', encoding='utf-8') as file:
    for line in file:
        line = json.loads(line)
        if i in list(range(500)):
            line_user_id_list_1.append(line['line_user_id'])
            i += 1
        elif i in list(range(500, 1000)):
            line_user_id_list_2.append(line['line_user_id'])
            i += 1
        elif i in list(range(1000, 1500)):
            line_user_id_list_3.append(line['line_user_id'])
            i += 1
        elif i in list(range(1500, 2000)):
            line_user_id_list_4.append(line['line_user_id'])
            i += 1
        elif i >= 2000:
            line_user_id_list_5.append(line['line_user_id'])
            i += 1

# print(list(range(1, 10)))
    # print(len(line_user_id_list_1))
    # print(len(line_user_id_list_2))
    # print(len(line_user_id_list_3))
    # print(len(line_user_id_list_4))
    # print(len(line_user_id_list_5))
    # print(line_user_id_list_5)

# # line_user_ref = db.collection(u'CloudMasterLineBotUser')
# # line_users = line_user_ref.stream()
# line_user_id_list = [user.to_dict()['line_user_id'] for user in line_users]

# # rich-menu
ref = db.collection(u'CloudMasterLineBotRichMenu').document(u'{}'.format("default"))
doc = ref.get()
rich_menu_id = doc.to_dict()['rich_menu_id']
print(rich_menu_id)

# # 對使用者綁定 default rich menu
line_bot_api = LineBotApi(channel_access_token="line access token")
line_bot_api.link_rich_menu_to_users(user_ids=line_user_id_list_1, rich_menu_id=rich_menu_id)
line_bot_api.link_rich_menu_to_users(user_ids=line_user_id_list_2, rich_menu_id=rich_menu_id)
line_bot_api.link_rich_menu_to_users(user_ids=line_user_id_list_3, rich_menu_id=rich_menu_id)
line_bot_api.link_rich_menu_to_users(user_ids=line_user_id_list_4, rich_menu_id=rich_menu_id)
line_bot_api.link_rich_menu_to_users(user_ids=line_user_id_list_5, rich_menu_id=rich_menu_id)

# # 修改資料庫內資料
for line_user_id in line_user_id_list_1:
    db.collection(u'CloudMasterLineBotUser').document(u'{}'.format(line_user_id)).update({"line_rich_menu_link_custom_name": "default"})
for line_user_id in line_user_id_list_2:
    db.collection(u'CloudMasterLineBotUser').document(u'{}'.format(line_user_id)).update({"line_rich_menu_link_custom_name": "default"})
for line_user_id in line_user_id_list_3:
    db.collection(u'CloudMasterLineBotUser').document(u'{}'.format(line_user_id)).update({"line_rich_menu_link_custom_name": "default"})
for line_user_id in line_user_id_list_4:
    db.collection(u'CloudMasterLineBotUser').document(u'{}'.format(line_user_id)).update({"line_rich_menu_link_custom_name": "default"})
for line_user_id in line_user_id_list_5:
    db.collection(u'CloudMasterLineBotUser').document(u'{}'.format(line_user_id)).update({"line_rich_menu_link_custom_name": "default"})