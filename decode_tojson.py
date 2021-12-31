#!/usr/bin/python
# -*- coding: utf-8 -*-

from flanker import mime
from bs4 import BeautifulSoup
from os import listdir
import json

# 大專院校字典
college_dict = {'政治大學': '國立政治大學', '清華大學': '國立清華大學', '臺灣大學': '國立臺灣大學', '臺灣師範': '國立臺灣師範大學', '成功大學': '國立成功大學', '中興大學': '國立中興大學', '陽明交通': '國立陽明交通大學', '中央大學': '國立中央大學', '中山大學': '國立中山大學', '臺灣海洋': '國立臺灣海洋大學', '中正大學': '國立中正大學', '高雄師範': '國立高雄師範大學', '彰化師範': '國立彰化師範大學', '臺北大學': '國立臺北大學', '嘉義大學': '國立嘉義大學', '高雄大學': '國立高雄大學', '東華大學': '國立東華大學', '暨南大學': '國立暨南國際大學', '臺灣科技': '國立臺灣科技大學', '雲林科技': '國立雲林科技大學', '屏東科技': '國立屏東科技大學', '臺北科技': '國立臺北科技大學', '臺北藝術': '國立臺北藝術大學', '臺灣藝術': '國立臺灣藝術大學', '臺東大學': '國立臺東大學', '宜蘭大學': '國立宜蘭大學', '聯合大學': '國立聯合大學', '虎尾科技': '國立虎尾科技大學', '臺南藝術': '國立臺南藝術大學', '臺南大學': '國立臺南大學', '臺北教育': '國立臺北教育大學', '臺中教育': '國立臺中教育大學', '澎湖科技': '國立澎湖科技大學', '勤益科技': '國立勤益科技大學', '體育大學': '國立體育大學', '臺北護理健康': '國立臺北護理健康大學', '高雄餐旅': '國立高雄餐旅大學', '金門大學': '國立金門大學', '臺灣體育運動': '國立臺灣體育運動大學', '臺中科技': '國立臺中科技大學', '臺北商業': '國立臺北商業大學', '屏東大學': '國立屏東大學', '高雄科技': '國立高雄科技大學', '東海大': '東海大學', '輔仁大': '輔仁大學', '東吳大': '東吳大學', '中原大': '中原大學', '淡江大': '淡江大學', '中國文化': '中國文化大學', '逢甲大': '逢甲大學', '靜宜大': '靜宜大學', '長庚大': '長庚大學', '元智大': '元智大學', '中華大': '中華大學', '大葉大': '大葉大學', '華梵大': '華梵大學', '義守大': '義守大學', '世新大': '世新大學', '銘傳大': '銘傳大學', '實踐大': '實踐大學', '朝陽科技': '朝陽科技大學', '高雄醫學': '高雄醫學大學', '南華大': '南華大學', '真理大': '真理大學', '大同大': '大同大學', '南臺科技': '南臺科技大學', '崑山科技': '崑山科技大學', '嘉南藥理': '嘉南藥理大學', '樹德科技': '樹德科技大學', '慈濟大': '慈濟大學', '臺北醫學': '臺北醫學大學', '中山醫學': '中山醫學大學', '龍華科技': '龍華科技大學', '輔英科技': '輔英科技大學', '明新科技': '明新科技大學', '長榮大': '長榮大學', '弘光科技': '弘光科技大學', '中國醫藥': '中國醫藥大學', '健行科技': '健行科技大學', '正修科技': '正修科技大學', '萬能科技': '萬能科技大學', '玄奘大': '玄奘大學', '建國科技': '建國科技大學', '明志科技': '明志科技大學', '高苑科技': '高苑科技大學', '大仁科技': '大仁科技大學', '聖約翰科技': '聖約翰科技大學', '嶺東科技': '嶺東科技大學', '中國科技': '中國科技大學', '中臺科技': '中臺科技大學', '亞洲大': '亞洲大學', '開南大': '開南大學', '佛光大': '佛光大學', '台南應用科技': '台南應用科技大學', '遠東科技': '遠東科技大學', '元培醫事科技': '元培醫事科技大學', '景文科技': '景文科技大學', '中華醫事科技': '中華醫事科技大學', '東南科技': '東南科技大學', '德明財經科技': '德明財經科技大學', '明道大': '明道大學', '南開科技': '南開科技大學', '中華科技': '中華科技大學', '僑光科技': '僑光科技大學', '育達科技': '育達科技大學', '美和科技': '美和科技大學', '吳鳳科技': '吳鳳科技大學', '環球科技': '環球科技大學', '台灣首府': '台灣首府大學', '中州科技': '中州科技大學', '修平科技': '修平科技大學', '長庚科技': '長庚科技大學', '臺北城市科技': '臺北城市科技大學', '敏實科技': '敏實科技大學', '醒吾科技': '醒吾科技大學', '文藻外語': '文藻外語大學', '華夏科技': '華夏科技大學', '慈濟科技': '慈濟科技大學', '致理科技': '致理科技大學', '康寧大': '康寧大學', '宏國德霖科技': '宏國德霖科技大學', '東方設計': '東方設計大學', '崇右影藝科技': '崇右影藝科技大學', '台北海洋科技': '台北海洋科技大學', '臺北市立': '臺北市立大學', '國立臺灣戲曲': '國立臺灣戲曲學院', '中信金融管理': '中信金融管理學院', '大漢技術': '大漢技術學院', '和春技術': '和春技術學院', '亞東技術': '亞東技術學院', '南亞技術': '南亞技術學院', '稻江科技暨管理': '稻江科技暨管理學院', '蘭陽技術': '蘭陽技術學院', '黎明技術': '黎明技術學院', '經國管理暨健康': '經國管理暨健康學院', '大同技術': '大同技術學院', '臺灣觀光': '臺灣觀光學院', '馬偕醫': '馬偕醫學院', '法鼓文理': '法鼓文理學院', '國立臺南護理': '國立臺南護理專科學校', '國立臺東': '國立臺東專科學校', '馬偕醫護管理': '馬偕醫護管理專科學校', '仁德醫護管理': '仁德醫護管理專科學校', '樹人醫護管理': '樹人醫護管理專科學校', '慈惠醫護管理': '慈惠醫護管理專科學校', '耕莘健康管理': '耕莘健康管理專科學校', '敏惠醫護管理': '敏惠醫護管理專科學校', '育英醫護管理': '育英醫護管理專科學校', '聖母醫護管理': '聖母醫護管理專科學校', '新生醫護管理': '新生醫護管理專科學校', '崇仁醫護管理': '崇仁醫護管理專科學校', '陽明大學':'國立陽明大學', '交通大學':'國立交通大學', '萬能技術':'萬能技術學院', '台中科技': '國立臺中科技大學', '台灣大學':'國立臺灣大學', '台灣師範':'國立臺灣師範大學', '台灣海洋':'國立臺灣海洋大學', '台北大學':'國立臺北大學', '台灣科技':'國立臺灣科技大學', '臺南應用科技':'台南應用科技大學', '臺灣首府':'台灣首府大學', '臺北海洋科技':'台北海洋科技大學', '台北科技':'國立臺北科技大學', '台北藝術':'國立臺北藝術大學', '台灣藝術':'國立臺灣藝術大學', '台東大學':'國立臺東大學', '台南藝術':'國立臺南藝術大學', '台南大學':'國立臺南大學', '台北教育':'國立臺北教育大學', '台中教育':'國立臺中教育大學', '台北護理健康':'國立臺北護理健康大學', '台灣體育運動':'國立臺灣體育運動大學', '台北商業':'國立臺北商業大學', '南台科技':'南臺科技大學', '台北醫學':'臺北醫學大學', '中台科技':'中臺科技大學', '台北城市科技':'臺北城市科技大學', '台北市立':'臺北市立大學', '台灣戲曲':'國立臺灣戲曲學院', '台灣觀光':'臺灣觀光學院', '台南護理專科':'國立臺南護理專科學校', '國立台東專科學校':'國立臺東專科學校'}





def eml_to_json(my_eml, myoutput):  # my_eml 是要讀取 (解析) 的 .eml 檔案
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
            # print(type(x))
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
                    print(count, record)                                                     ###################print#######################
                    d["platform"] = "1111"
                    if "代碼" in record and "完整履歷" in record:   # 以下皆為將資料放到 d 字典裏面                        
                        if "(９大職能星測評)" in record:
                            d["id"] = record.split("代碼")[1].split("(９大職能星測評)")[0]
                        else:
                            d["id"] = record.split("代碼")[1].split("完整履歷")[0]
                    
                        d["name"] = record.split("代碼")[0]
                    # 如果 json 有那個人的代碼了，不要存
                        try:
                            for line in open(myoutput, 'r', encoding="utf-8"):
                                tweet = json.loads(line)
                                if tweet["id"] in record:
                                    d["id"] = ""
                        except FileNotFoundError:
                            pass


                    if("男性" in record) or ("女性" in record):
                        d["gender"] = record.split("|")[0]
                    if "gender" not in d.keys():    # 如果字典裡沒有性別，代表沒有檢測到男性或女性，則為多元性別
                        d["gender"] = "多元性別"

                    if "歲" in record and "|" in record:  
                        d["age"] = int(record.split("|")[1].replace("歲", ""))
                        if d["age"] == "":  # 若年齡為空值...
                            d["age"] = 999
                    if "age" not in d.keys():  # 如果字典裡沒有年齡，代表沒有檢測到"歲"，則為"999歲"異常
                        d["age"] = 999

                    if "聯絡電話" in record:
                        cell_phones = []
                        phones = record.split("聯絡電話")[1].split("|")[:]                        
                        for cell_phone in phones:
                            if cell_phone.startswith("09"):
                                cell_phones.append(cell_phone)
                                d["cell_phone"] = cell_phones
                        if d["cell_phone"] == []:
                            d["cell_phone"] = ["無"]
                    if "cell_phone" not in d.keys():
                        d["cell_phone"] = ["無"]

                    if "電子郵件" in record:
                        d["email"] = record.split("電子郵件")[1]
                        if d["email"] == "":
                            d["email"] = "無"
                    if "email" not in d.keys():
                        d["email"] = "無"

                    if "聯絡地址" in record:
                        d["address"] = record.split("聯絡地址")[1]
                        if d["address"] == "":
                            d["address"] = "無"
                    if "address" not in d.keys():
                        d["address"] = "無"

                    if "教育程度" in record:
                        try:
                            department = record.split("(")[1]
                            d["edu_level"] = record.split("教育程度")[1][:2]
                            d["edu_status"] = record.split("教育程度")[1][2:4]
                            # d["edu_department"] = department.replace(")", "")

                            try:
                                for i in college_dict.keys():
                                    if i in record:
                                        d["edu_school"] = college_dict[i]
                                        break
                                    else:
                                        d["edu_school"] = record.split("教育程度")[1][4:].replace("("+department, "")
                            except:
                                d["edu_school"] = record.split("教育程度")[1][4:].replace("("+department, "")
                        except:
                            try:
                                d["edu_level"] = record.split("教育程度")[1][:2]
                                d["edu_status"] = record.split("教育程度")[1][2:4]
                                for i in college_dict.keys():
                                    if i in record:
                                        d["edu_school"] = college_dict[i]
                                        break
                                    else:
                                        d["edu_school"] = record.split("教育程度")[1][4:]

                            except:
                                d["edu_level"] = "無"
                                d["edu_status"] = "無"
                                d["edu_school"] = "無"
                                d["edu_department"] = "無"
                    if "類)" in record:
                        d["edu_department"] = record.split("(")[1].replace(")", "")
                    # 如果沒有掃到教育程度 給無
                    if "edu_level" not in d:
                        d["edu_level"] = "無"
                    if "edu_status" not in d:
                        d["edu_status"] = "無"
                    if "edu_school" not in d:
                        d["edu_school"] = "無"
                    if "edu_department" not in d:
                        d["edu_department"] = "無"



                    if "職務類別" in record:
                        d["wanted_job_titles"] = record.split("職務類別")[1].split("，")[:]
                        if d["wanted_job_titles"] == "" or d["wanted_job_titles"] == []:
                            d["wanted_job_titles"] = ["無"]
                    if "wanted_job_titles" not in d.keys():
                        d["wanted_job_titles"] = ["無"]

                    if "期望產業" in record:
                        d["wanted_jot_types"] = record.split("期望產業")[1].split("，")[:]
                        if d["wanted_jot_types"] == "" or d["wanted_jot_types"] == []:
                            d["wanted_jot_types"] = ["無"]
                    if "wanted_jot_types" not in d.keys():
                        d["wanted_jot_types"] = ["無"]

                    if "上班地點" in record:
                        d["wanted_job_locations"] = record.split("上班地點")[1].split("，")[:]
                        if d["wanted_job_locations"] == "" or d["wanted_job_locations"] == []:
                            d["wanted_job_locations"] = "無"
                    if "wanted_job_locations" not in d.keys():
                        d["wanted_job_locations"] = "無"


                    if "工作經驗累計年資" in record:
                        if "無工作經驗" not in record:
                            try:
                                work_min_year = int(record.split("工作經驗累計年資")[1].split("~")[0])
                                d["working_months"] = int(work_min_year * 12)
                                if d["working_months"] == "":
                                    d["working_months"] = "無"
                            except:
                                d["working_months"] = "待業中"
                        else:
                            d["working_months"] = "無工作經驗"
                    if "working_months" not in d.keys():
                        d["working_months"] = "無"

                    if "累計經驗" in record:
                        experiences = record.split("累計經驗")[1].split("|")
                        exp_l = []
                        job_list = []
                        for experience in experiences:
                            exp_d = {}
                            try:
                                exp_d["title"] = "".join([title for title in experience if not title.isdigit()]).replace("~", "").replace("年", "")
                                duration = [year for year in experience if year.isdigit()]
                                if len(duration) == 2:
                                    exp_d["duration"] = "~".join([year for year in experience if year.isdigit()]) + "年"
                                elif len(duration) == 3:
                                    exp_d["duration"] = duration[0] + "~" + duration[1] + duration[2] + "年"  # 已改
                                else:
                                    exp_d["duration"] = duration[0] + duration[1] + "~" + duration[2] + duration[3] + "年"
                                exp_l.append(exp_d)
                            except:
                                exp_d["title"] = "".join([title for title in experience if not title.isdigit()]).replace("~", "").replace("年", "")
                                exp_d["duration"] = "無"
                                exp_l.append(exp_d)
                            d["work_experiences"] = exp_l
                        if d["work_experiences"] == "" or d["work_experiences"] == [] or "work_experiences" not in d.keys():
                            d["work_experiences"] = "無"                        
                        
                        try:
                            past_jobs = ",".join(sub_list[count+1:]).split(",專長")[0]
                            past_jobs_list = past_jobs.split(",")
                            for job in past_jobs_list:
                                # print(job)
                                if not job.isdigit():
                                    job_dict = {}
                                    job_dict["title"] = job.split("（")[0] 
                                    try:
                                        job_dict["duration"] = job.split("（")[1].split("）")[0]
                                    except:
                                        job_dict["duration"] = "無"
                                    try:
                                        job_dict["location"] = job.split("(")[1].split(")")[0]
                                    except:
                                        job_dict["location"] = "無"
                                    try:
                                        job_dict["date"] = job.split(")")[1]
                                    except:
                                        job_dict["date"] = "無"
                                    job_list.append(job_dict)
                            d["work_experience_list"] = job_list
                        except:
                            d["work_experience_list"] = "無"

                    if "語文專長" in record:
                        lang_list = []
                        for i in record.split("[")[1:]:
                            lan_dict = {}
                            lan_dict["language"] = i.split("]")[0]
                            lan_dict["listen"] = i.split("聽-")[1].split("|")[0]
                            lan_dict["speak"] = i.split("說-")[1].split("|")[0]
                            lan_dict["read"] = i.split("讀-")[1].split("|")[0]
                            lan_dict["write"] = i.split("寫-")[1]
                            lang_list.append(lan_dict)
                        d["languages"] = lang_list
                        if d["languages"] == "" or d["languages"] == []:
                            lang_list = []
                            for i in record.split("[")[1:]:
                                lan_dict = {}
                                lan_dict["language"] = "無"
                                lan_dict["listen"] = "無"
                                lan_dict["speak"] = "無"
                                lan_dict["read"] = "無"
                                lan_dict["write"] = "無"
                                lang_list.append(lan_dict)
                            d["languages"] = lang_list

                    if "languages" not in d.keys():
                        lang_list = []
                        lan_dict = {}
                        lan_dict["language"] = "無"
                        lan_dict["listen"] = "無"
                        lan_dict["speak"] = "無"
                        lan_dict["read"] = "無"
                        lan_dict["write"] = "無"
                        lang_list.append(lan_dict)
                        d["languages"] = lang_list

                    if "電腦專長" in record:
                        computer_list = []
                        for i in record.split("電腦專長")[1].split("，")[:]:
                            computer_list.append(i)
                        d["computer_expertises"] = computer_list
                        if d["computer_expertises"] == "" or d["computer_expertises"] == []:
                            d["computer_expertises"] = ["無"]
                    if "computer_expertises" not in d.keys():
                        d["computer_expertises"] = ["無"]

                if d["id"] == "":
                    continue
                if d["name"] == "":  # 如果姓名是空值，捨棄這個人的資料
                    continue

                with open(myoutput, 'a', encoding="utf-8") as fout:
                    json.dump(d, fout, ensure_ascii=False)
                    fout.write("\n")

                # return d  # coll 長相 [{...}]
        
# eml 擋存放目錄
mypath = ".//eml_test"
output = "output_test.json"

# 取的目錄下所有 eml 擋存入 list
files = listdir(mypath)  # 列出資料夾每個檔案的名字與檔案類型

# 讀擋並處理轉換 csv
for count , file in enumerate(files):
    print(file)
    result = eml_to_json(mypath + "/" + file, output)

    # break


    # with open(myoutput, 'a', encoding="utf-8") as fout:
    #     json.dump(result, fout, ensure_ascii=False)
    #     fout.write("\n")

