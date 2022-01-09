# -*- coding: UTF-8 -*-
from daos.mail_dao import AbstractMailDao
from google.cloud import storage
from dotenv import load_dotenv
import os
from models.email import Email


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
        """Save email data on GCP Cloud Storage
        """
        subject = mail.subject
        body_text = mail.body_text
        body_html = mail.body_html
        create_time = mail.create_time
        create_time = str(create_time).split(".")[0].replace("-", "").replace(" ","").replace(":","")

        storage_client = storage.Client()
        load_dotenv()
        bucket_name = os.getenv("bucket_name")

        with open("/tmp/email_subject.txt", "w", encoding="utf-8") as sub:
                sub.write(subject + "\n")
        with open("/tmp/email_text.txt", "w", encoding="utf-8") as tx:
            tx.write(body_text + "\n")
        with open("/tmp/email_html.txt", "w", encoding="utf-8") as htl:
            htl.write(body_html + "\n")
        
        MailStorageDao.upload(bucket_name, "email/"+create_time+"/"+"email_subject.txt", "/tmp/email_subject.txt")
        MailStorageDao.upload(bucket_name, "email/"+create_time+"/"+"email_text.txt", "/tmp/email_text.txt")
        MailStorageDao.upload(bucket_name, "email/"+create_time+"/"+"email_html.txt", "/tmp/email_html.txt")

        os.remove("/tmp/email_subject.txt")
        os.remove("/tmp/email_text.txt")
        os.remove("/tmp/email_html.txt")
        return "OK"
