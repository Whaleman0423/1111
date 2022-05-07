import csv
import json
import pandas as pd

from google.cloud import firestore

# 使用前先改確認讀取的 csv 路徑、金鑰、專案id

# db = firestore.Client()
db = firestore.Client.from_service_account_json("./cloud-master-3-29-cfb7e9371055.json", project='cloud-master-3-29')

# 開啟 CSV 檔案
with open('aws_cp_考古題_總題庫_csv.csv', newline='', encoding="utf-8") as csvfile:

  # 讀取 CSV 檔案內容
  rows = csv.reader(csvfile)
  next(rows, None)  # skip the headers
  print(type(rows))
  i = 0
  list_ = []
  # 以迴圈輸出每一列
  for row in rows:
    print(i)
    # row => [question_id, question_content, question_cn_content, A, B, C, D, true_answer, CN_A, CN_B, CN_C, CN_D, detail_explain, expert_comment, question_domain_attribute, question_architecture_attribute, question_servcie_attribute]
    if row[0] == "":  # 遇到沒有 id 的就跳下一個
        continue
    d = {}
    d["question_id"] = row[0]
    d["question_content"] = row[1]
    d["question_cn_content"] = row[2]
    #選項
    d["question_choices"] = []
    d["question_choices"].append({"answer_alias":"A","content":row[3].replace("(A)",""), "correct": False})
    d["question_choices"].append({"answer_alias":"B","content":row[4].replace("(B)",""), "correct": False})
    d["question_choices"].append({"answer_alias":"C","content":row[5].replace("(C)",""), "correct": False})
    d["question_choices"].append({"answer_alias":"D","content":row[6].replace("(D)",""), "correct": False})
    # 中文選項
    d["question_cn_choices"].append({"answer_alias":"A","content":row[8].replace("(A)",""), "correct": False})
    d["question_cn_choices"].append({"answer_alias":"B","content":row[9].replace("(B)",""), "correct": False})
    d["question_cn_choices"].append({"answer_alias":"C","content":row[10].replace("(C)",""), "correct": False})
    d["question_cn_choices"].append({"answer_alias":"D","content":row[11].replace("(D)",""), "correct": False})
    for ans in row[7]:
      if ans == "A":
        d["question_choices"][0]["correct"] = True
        d["question_cn_choices"][0]["correct"] = True
      elif ans == "B":
        d["question_choices"][1]["correct"] = True
        d["question_cn_choices"][1]["correct"] = True
      elif ans == "C":
        d["question_choices"][2]["correct"] = True
        d["question_cn_choices"][2]["correct"] = True
      elif ans == "D":
        d["question_choices"][3]["correct"] = True
        d["question_cn_choices"][3]["correct"] = True
    d["detail_explain"] = row[12]
    d["expert_comment"] = row[13]
    d["question_attribute"] = [row[14], row[15], row[16]]

# 儲存 json
    with open("CloudMasterExamQuestionAwsCp.json", 'a', encoding="utf-8") as fout:
      json.dump(d, fout, ensure_ascii=False)
      fout.write("\n")
# 上傳 firestore
    db.collection(u'CloudMasterExamQuestionAwsCp').document(str(i)).set(d)
    i += 1
    list_.append(d)

# 都上傳完畢後，查看目前 Firestore 資料集 CloudMasterExamQuestionAwsCp 有幾筆檔案
exams_qa_ref = db.collection(u'CloudMasterExamQuestionAwsCp')
docs = exams_qa_ref.stream()
n = 0
for doc in docs:
  n +=1
print('總題數: ', n, '題')
db.collection(u'CloudMasterExam').document(u'CloudMasterExamQuestionAwsCp').set({
  u'exam_name': u'CloudMasterExamQuestionAwsCp',
  u'deduct_point_amount': 1,
  u'number_of_questions': n,
  u'stat_name': u'CloudMasterExamQuestionAwsCpUserStat'
})

# 儲存CSV
df = pd.json_normalize(list_)

df.to_csv("CloudMasterExamQuestionAwsCp.csv")