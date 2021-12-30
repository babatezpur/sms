import os, twilio
from twilio.rest import Client
import mysql.connector
from mysql.connector import MySQLConnection


def send_sms(to_number,message):
    print("message is : "+str(message))
    account_sid = '###'
    auth_token = '###'
    twilio_number = "+###"

    client = Client(account_sid, auth_token)
    msg=client.messages.create(body=message,from_=twilio_number,to=to_number)

db = mysql.connector.connect(user='retainiqadmin', password='retainiq', host='reatainiq.cijb4cmptrmk.us-east-1.rds.amazonaws.com',database='retainiqdb')
cursor = db.cursor()
query="select * from message_schedule where template_name like 'sms%' and current_status='N' and url like 'https://perforacare.com%' and time_delay<CONVERT_TZ(NOW(),'SYSTEM','Asia/Calcutta') order by template_id desc "
cursor.execute(query)
result=cursor.fetchall()
for row in result:
    cart_url=row[9]
    template_id=row[7]
    serial_no=row[0]
    name_query=(
        "select  merchant_name,shipping_address_first_name,shipping_address_phone "
        "from abandoned_checkouts_by_day t1,merchants t2 where t1.merchant_id=t2.id "
        "and abandoned_checkout_url=%s"
        )
    cursor.execute(name_query,(cart_url,))
    name_row=cursor.fetchall()
    merchant_name=name_row[0]
    shipping_address_first_name=name_row[1]
    shipping_address_phone=name_row[2]

    query1= "select id from url_redirects where cart_url = %s"
    cursor.execute(query1,(cart_url,))
    redirect_result=cursor.fetchall()
    try:
        redirect_url=redirect_result[0]
        cart_url="http://re10.co/?i="+redirect_url+"&serialno="+serial_no
        print(cart_url)
        print(template_id)
        if template_id=='template1':
            print("message is "+message)
            message="Perfora: Hi "+shipping_address_first_name+", it's your friends at Perfora!"
            message+="Looks like you didn't quite make it through checkout, but we saved your cart for you!"
            message+="Don't forget, Perfora orders are 100% guaranteed, so you can try us risk-free 😀"
            message+=cart_url
            print("calling send_sms")
            send_sms(shipping_address_phone, message)
            db = mysql.connector.connect(user='retainiqadmin', password='retainiq', host='reatainiq.cijb4cmptrmk.us-east-1.rds.amazonaws.com',database='retainiqdb')
            cursor = db.cursor()
            query_update="update message_schedule set current_status ='Y' where serial_no=%s"
            cursor.execute(query_update,(serial_no,))
            db.commit()
        if template_id=='template2':
            message="Perfora: It's fine, we're fine. We know how busy you are, and we love that about you. Last text and we won't ask again. Your exclusive coupon code 7qavbJdRuI4J for 25% off expires in next 3 hours "
            message+=cart_url
            print("calling send_sms")
            send_sms(shipping_address_phone,message)
            db = mysql.connector.connect(user='retainiqadmin', password='retainiq', host='reatainiq.cijb4cmptrmk.us-east-1.rds.amazonaws.com',database='retainiqdb')
            cursor = db.cursor()
            query_update="update message_schedule set current_status ='Y' where serial_no=%s"
            cursor.execute(query_update,(serial_no,))
            db.commit()
    except:
        continue
