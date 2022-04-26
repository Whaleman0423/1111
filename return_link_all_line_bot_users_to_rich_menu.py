from google.cloud import firestore
from linebot import LineBotApi
import json

# 功能：將 CloudMasterLineBotUser.json 的所有用戶，若超過 500 人, 則分批用 line bot api 綁定指定的圖文選單

# 請先更新 第 9 行 line access token、確認第 13 行的檔案存在、補上第 27 行的 rich_menu_id

line_bot_api = LineBotApi(channel_access_token="line access token")

line_user_ids_list = []

with open('CloudMasterLineBotUser.json', 'r', encoding='utf-8') as file:
    for line in file:
        line = json.loads(line)
        line_user_ids_list.append(line['line_user_id'])
    
    # 用戶總數
    num_of_line_users = len(line_user_ids_list)
    set_of_list = num_of_line_users // 500 + 1
    start = 0
    end = 500
    for i in range(set_of_list):
        if end > num_of_line_users:
            end = num_of_line_users
            sub_list = line_user_ids_list[start: end]
            line_bot_api.link_rich_menu_to_users(user_ids=sub_list, rich_menu_id= )
