from flanker import mime
from bs4 import BeautifulSoup
from os import listdir
import csv

def eml_to_list(my_eml):  # my_eml 是要讀取 (解析) 的 .eml 檔案
    with open(my_eml, 'rb') as fhdl:  # 開啟 eml 檔案
        raw_email = fhdl.read()  # 讀取 eml 檔案
    msg = mime.from_string(raw_email)  # mime.from_string 是用來解析 MIME 訊息的，eml 就是遵從 MIME  # 信件內容是屬於 multi-parts 多部份組成
    for part in msg.parts:  # 因為信件內容有分很多個 part，所以需一個一個部分取出
        container = []
        container2 = []
        if(part.content_type == "text/html"):   # 若有 part 的 content_type 是屬於 text/html 格式的 
            soup = BeautifulSoup(part.body, "html.parser")  # 使用 beautifilsoup 解析，跟爬蟲一樣
            res = soup.table.table  # 選出 table 標籤
            x = res.find_all("tr")  # 找出所有 tr 標籤，return ResultSet 是一種 list 的子類，可以遍歷  
            print(type(x))
            for item in x:  # 遍歷 tr 標籤
                q = item.text.replace(" ","").replace('\u3000',"").replace('▍',"").splitlines()  # 取出 <tr>標籤 裡面的text 並將空格等的地方去掉，splitlines 的功能是 將有換行的以 list 格式列出
                container.append(q)  # 將每個 tr 清洗的結果放到 container
            v = list(filter(lambda x: x, container))  # 將列表為空的篩選掉，不知道怎麼做的
            v.pop()  # 移除 清單最後一個元素

            split_resumes = []
            coll = []
            for i in v:
                container2.append(i[0])   # 取出 v清單 每個元素去掉清單[]留下字串 並放到 container2 
            container2.pop(0) 
            container2.pop(0)  # 去掉 container2 清單前兩個元素
            container2.pop()  # 去掉 containe2 清單最後一個元素
            result = ','.join(container2)  # 將清單轉成字串，並用逗號隔開
            info = result.split("最後修改")  # 將字串轉成清單，並用 "最後修改"為分隔

            for s in info:
                if(len(s) < 100):  # 將 info 清單裡面的每個元素遍歷，字串超過100字的留下，少於100字的刪除  => 僅留下要取資料的字串 (裡面有我們要的姓名、性別、年齡...的資料)
                    info.remove(s)
            
            for x in info:
                record = x.split(",")  # 將清單中每個元素(都是字串)轉換成以","分隔的清單
                record.pop(0)  
                record.pop(0)  # 去掉前兩個元素
                split_resumes.append(record)
            mytest = list(filter(lambda y: y ,split_resumes))  # 再次移除掉空的清單，移除後剩兩個元素，都是清單
            for sub_list in mytest:
                d = {}
                if(len(sub_list[-1]) <= 5):
                    sub_list.pop()  # 移除掉清單中的最後一個元素 ''
                for count , record in enumerate(sub_list):  # 每一個元素給予標號
                    # print(count, record)
                    if "代碼" in record:   # 以下皆為將資料放到 d 字典裏面                        
                        if "(９大職能星測評)" in record:
                            d["代碼"] = record.split("代碼")[1].split("(９大職能星測評)")[0]
                        else:
                            d["代碼"] = record.split("代碼")[1].split("完整履歷")[0]
                        d["姓名"] = record.split("代碼")[0]
                        if d["姓名"] == "":  # 如果姓名是空值，捨棄這個人的資料
                            break


                    if("男性" in record) or ("女性" in record):
                        d["性別"] = record.split("|")[0]
                    if "性別" not in d.keys():    # 如果字典裡沒有性別，代表沒有檢測到男性或女性，則為多元性別
                        d["性別"] = "多元性別"

                    if "歲" in record:  
                        d["年齡"] = record.split("|")[1]
                        if d["年齡"] == "" or d["年齡"] == "歲":  # 若年齡為空值...
                            d["年齡"] = "999歲"
                    if "年齡" not in d.keys():  # 如果字典裡沒有年齡，代表沒有檢測到"歲"，則為"999歲"異常
                        d["年齡"] = "999歲"

                    if "聯絡電話" in record:
                        d["聯絡電話"] = record.split("聯絡電話")[1]
                        if d["聯絡電話"] == "":
                            d["聯絡電話"] = "無"
                    if "聯絡電話" not in d.keys():
                        d["聯絡電話"] = "無"


                    if "電子郵件" in record:
                        d["電子郵件"] = record.split("電子郵件")[1]
                        if d["電子郵件"] == "":
                            d["電子郵件"] = "無"
                    if "電子郵件" not in d.keys():
                        d["電子郵件"] = "無"

                    if "聯絡地址" in record:
                        d["聯絡地址"] = record.split("聯絡地址")[1]
                        if d["聯絡地址"] == "":
                            d["聯絡地址"] = "無"
                    if "聯絡地址" not in d.keys():
                        d["聯絡地址"] = "無"

                    if "教育程度" in record:
                        d["教育程度"] = record.split("教育程度")[1]
                        if d["教育程度"] == "":
                            d["教育程度"] = "無"
                    if "教育程度" not in d.keys():
                        d["教育程度"] = "無"

                    if "職務類別" in record:
                        d["求職類別"] = record.split("職務類別")[1]
                        if d["求職類別"] == "":
                            d["求職類別"] = "無"
                    if "求職類別" not in d.keys():
                        d["求職類別"] = "無"

                    if "上班地點" in record:
                        d["上班地點"] = record.split("上班地點")[1]
                        if d["上班地點"] == "":
                            d["上班地點"] = "無"
                    if "上班地點" not in d.keys():
                        d["上班地點"] = "無"


                    if "工作經驗累計年資" in record:
                        if "無工作經驗" not in record:
                            work_min_year = int(record.split("工作經驗累計年資")[1].split("~")[0])
                            d["累計年資"] = str(work_min_year * 12) + " 月"
                            if d["累計年資"] == "":
                                d["累計年資"] = "99"
                        else:
                            d["累計年資"] = "無工作經驗"
                    if "累計年資" not in d.keys():
                        d["累計年資"] = "99"

                    if "累計經驗" in record:
                        d["累計經驗"] = record.split("累計經驗")[1]
                        if d["累計經驗"] == "":
                            d["累計經驗"] = "無"
                        try:
                            d["過往公司"] = ",".join(sub_list[count+1:]).split(",專長")[0]
                        except:
                            d["過往公司"] = ",".join(sub_list[count+1:])
                        if d["過往公司"] == "":
                            d["過往公司"] = "無"

                    if "語文專長" in record:
                        d["語文專長"] = record.split("語文專長")[1]
                        if d["語文專長"] == "":
                            d["語文專長"] = "無"
                    if "語文專長" not in d.keys():
                        d["語文專長"] = "無"

                    if "電腦專長" in record:
                        d["電腦專長"] = record.split("電腦專長")[1]
                        if d["電腦專長"] == "":
                            d["電腦專長"] = "無"
                    if "電腦專長" not in d.keys():
                        d["電腦專長"] = "無"


                coll.append(d)  # 將字典 d 放到 coll清單
            return coll  # coll 長相 [{...}]
        
# eml 擋存放目錄
mypath = ".//eml"
myoutput = "output.csv"
fieldnames = ['代碼', '姓名', '性別', '年齡','聯絡電話','電子郵件','聯絡地址','教育程度','求職類別', "上班地點",'累計年資','累計經驗','過往公司', "語文專長", "電腦專長"]

# 取的目錄下所有 eml 擋存入 list
files = listdir(mypath)  # 列出資料夾每個檔案的名字與檔案類型

# 讀擋並處理轉換 csv
for count , file in enumerate(files):
    result = eml_to_list(mypath + "/" + file)
    with open(myoutput, 'a', newline='', encoding='utf-8-sig') as csvfile:   # 使用 utf-8-sig 編碼，才不會出現錯誤，手動開 csv 也是可讀的，不是亂碼
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if count == 0:
            writer.writeheader()  # 第一個檔案要加
        for i in result:
            writer.writerow(i)
    # break
