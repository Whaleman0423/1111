import csv
import json
import pandas as pd

from google.cloud import firestore

# 使用前先改確認讀取的 csv 路徑、金鑰、專案id

# db = firestore.Client()
db = firestore.Client.from_service_account_json("./cloud-master-3-29-cfb7e9371055.json", project='cloud-master-3-29')

# 開啟 CSV 檔案
with open('aws_clf_考古題_總題庫_csv.csv', newline='', encoding="utf-8") as csvfile:

  # 讀取 CSV 檔案內容
    rows = csv.reader(csvfile)
    next(rows, None)  # skip the headers
    # print(type(rows))
    i = 0
    list_ = []

  # 以迴圈輸出每一列
    for row in rows:
        print(i)
        # row => [question_id, question_content, question_cn_content, A, B, C, D, true_answer, CN_A, CN_B, CN_C, CN_D, detail_explain, expert_comment, question_domain_attribute, question_architecture_attribute, question_servcie_attribute]
        if row[0] == "":  # 遇到沒有 id 的就跳下一個
            continue
        # 建立用來放答案的清單
        question_choices = row[3: 7]
        
        # 建立用來放中文答案的清單
        question_cn_choices = row[8: 12]

        del row[3: 7]
        row.insert(3, question_choices)
        del row[5: 9]
        row.insert(5, question_cn_choices)
        # print(row)
        # break
        keys = ["question_id", "question_content", "question_cn_content", "question_choices", "true_answer", "question_cn_choices", "detail_explain", "expert_comment", "question_attribute"]
        
        d = {keys[i]:row[i] for i in range(9)}
        d["question_attribute"] = [row[8], row[9], row[10]]
# 儲存 json
        with open("ExamQuestionAwsClf.json", 'a', encoding="utf-8") as fout:
            json.dump(d, fout, ensure_ascii=False)
            fout.write("\n")
# 上傳 firestore
        db.collection(u'ExamQuestionAwsClf').document(str(i)).set(d)
        i += 1
        list_.append(d)

# 儲存CSV
df = pd.json_normalize(list_)

df.to_csv("ExamQuestionAwsClf.csv")