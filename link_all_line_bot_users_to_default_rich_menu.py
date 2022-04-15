from google.cloud import firestore
from linebot import LineBotApi

db = firestore.Client()

# line-bot user
line_user_ref = db.collection(u'CloudMasterLineBotUser')
line_users = line_user_ref.stream()
line_user_id_list = [user.to_dict()['line_user_id'] for user in line_users]

# rich-menu
ref = db.collection(u'CloudMasterLineBotRichMenu').document(u'{}'.format("default"))
doc = ref.get()
rich_menu_id = doc.to_dict()['rich_menu_id']

# 對使用者綁定 default rich menu
line_bot_api = LineBotApi(channel_access_token="LINE_BOT_CHANNEL_ACCESS_TOKEN")
line_bot_api.link_rich_menu_to_users(user_ids=line_user_id_list, rich_menu_id=rich_menu_id)

# 修改資料庫內資料
for line_user_id in line_user_id_list:
    db.collection(u'CloudMasterLineBotUser').document(u'{}'.format(line_user_id)).update({"line_rich_menu_link_custom_name": "default"})