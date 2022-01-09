# -*- coding: UTF-8 -*-
from daos.mail_dao import AbstractMailDao
import datetime
from google.cloud import storage
from dotenv import load_dotenv
import os

class MailStorageDao(AbstractMailDao):
    """Email 對 GCP Cloud Storage 的操作
    
    TODO: 實作 add 方法
          將 Email 儲存至 GCP Cloud Storage
    add 方法接收 Email 物件
    
    要上傳至
        bucket name：cloud-course-ad-system
        object name：email/YYYYMMDDHHMM/檔名.副檔名
    bucket name 請用 env 設定檔帶入

    將電子郵件的主旨存成 email_subject.txt
    將電子郵件的純文字內容存成 email_text.txt
    將電子郵件的html內容存成 email_html.txt

    將以上檔案上傳到 GCP Cloud Storage
    如成功上傳，回傳字串 OK
    
    範例：
    /cloud-course-ad-system/
        email/
            202201072359/
                  email_subject.txt
                  email_text.txt
                  email_html.txt
                  target.json
    """
    @classmethod
    def check_file_exist_or_not(cls, bucket_name, name):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        stats = storage.Blob(bucket=bucket, name=name).exists(storage_client)
        return stats

    @classmethod
    def download(cls, bucket_name, source_blob_name, destination_file_name)
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
        except:
            print("{} 下載失敗".format(source_blob_name))
    
    @classmethod
    def upload(cls, bucket_name, destination_blob_name, source_file_name):
        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
        except:
            print("{} 上傳失敗".format(source_file_name))

    @classmethod
    def add(cls, mail: Email):
        """Save email data on GCP Cloud Storage"""
        subject = mail.subject
        body_text = mail.body_text
        body_html = mail.body_html
        date_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        
        # 先確認桶子內有沒有時間目錄
        storage_client = storage.Client()
        # 載入 bucket name .env檔案
        load_dotenv()
        bucket_name = os.getenv("bucket_name")
        # 目錄名為 時間 
        name = "email/" + date_time + "/"
        stats = MailStorageDao.check_file_exist_or_not(bucket_name, name)
        
        # 如果存在，stats 為 True，下載資料夾內的檔案到 /tmp
        if stats:
            print("時間目錄存在")
            # 嘗試下載 email_subject.txt
            MailStorageDao.download(bucket_name, name+"email_subject.txt", "/tmp/email_subject.txt")
            MailStorageDao.download(bucket_name, name+"email_text.txt", "/tmp/email_text.txt")
            MailStorageDao.download(bucket_name, name+"email_html.txt", "/tmp/email_html.txt")
            # "a" 附加寫入 .txt檔案 
            with open("/tmp/email_subject.txt", "a", encoding="utf-8") as sub:
                sub.write(subject + "\n")
            with open("/tmp/email_text.txt", "a", encoding="utf-8") as tx:
                tx.write(body_text + "\n")
            with open("/tmp/email_html.txt", "a", encoding="utf-8") as htl:
                htl.write(body_html + "\n")
            # 將 .txt檔案 上傳回去 bucket
            MailStorageDao.upload(bucket_name, name+"email_subject.txt", "/tmp/email_subject.txt")
            MailStorageDao.upload(bucket_name, name+"email_text.txt", "/tmp/email_text.txt")
            MailStorageDao.upload(bucket_name, name+"email_html.txt", "/tmp/email_html.txt")
            # 刪除暫存檔案
            os.remove("/tmp/email_subject.txt")
            os.remove("/tmp/email_text.txt")
            os.remove("/tmp/email_html.txt")
        except:  # 如果沒有該時間目錄
            with open("/tmp/email_subject.txt", "a", encoding="utf-8") as sub:
                sub.write(subject + "\n")
            with open("/tmp/email_text.txt", "a", encoding="utf-8") as tx:
                tx.write(body_text + "\n")
            with open("/tmp/email_html.txt", "a", encoding="utf-8") as htl:
                htl.write(body_html + "\n")
            MailStorageDao.upload(bucket_name, name+"email_subject.txt", "/tmp/email_subject.txt")
            MailStorageDao.upload(bucket_name, name+"email_text.txt", "/tmp/email_text.txt")
            MailStorageDao.upload(bucket_name, name+"email_html.txt", "/tmp/email_html.txt")
            os.remove("/tmp/email_subject.txt")
            os.remove("/tmp/email_text.txt")
            os.remove("/tmp/email_html.txt")
        return "OK"
