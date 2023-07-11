from flask import Flask,send_file, render_template, request, jsonify, make_response, send_from_directory, redirect, url_for
import os
import io
import zipfile
from werkzeug.utils import secure_filename
from os.path import exists

version_file = open("/home/pi/firmware/SERVICE_VERSION",'w')
version_file.write("0.0.2")
version_file.close()
os.chown('/home/pi/firmware/SERVICE_VERSION',1000,1000)
app = Flask(__name__)

@app.route('/get_info',methods=['GET'])
def about_device():
    if request.method == 'GET':
        if not exists("/home/pi/firmware/system_info") :
            return ""

        f = open("/home/pi/firmware/system_info","r")
        info = f.read()
        f.close()
        return info

@app.route('/delete_report', methods=['POST'])
def delete_report():
    if request.method == 'POST':
        password=request.values['password']
        if (password==""):
           return "input empty!"
        elif (password=="Honestmc"):
           os.system("cd /home/pi/report;ls;rm -rf /home/pi/report/*;ls")
           return "success!"
        else :
           return "input error"

@app.route('/update', methods=['GET','POST'])
def update_fw():
    if request.method == 'POST':
        password=request.values['password']
        if (password==""):
            return "input empty!"
        elif (password=="Honestmc"):

            md5tag = request.values['md5tag']
            md5path = open('/home/pi/tmp/UPDATE.md5tag','w')
            md5path.write(md5tag)
            md5path.close()
            os.chown('/home/pi/tmp/UPDATE.md5tag',1000,1000)

            file = request.files['file']
            filename = secure_filename(file.filename)
            file.save(os.path.join('/home/pi/tmp', filename))
            os.chown('/home/pi/tmp/'+filename,1000,1000)

            update = open('/home/pi/tmp/UPDATE_WIFI_MODE','w')
            update.write("")
            update.close()
            os.chown('/home/pi/tmp/UPDATE_WIFI_MODE',1000,1000)

            return "success!"
        else :
            return "password error"
    if request.method == 'GET':
        if os.path.exists('/home/pi/firmware/SYS_MD5'):
            md5_date_f = open("/home/pi/firmware/SYS_MD5",'r')
            date = md5_date_f.read()
            md5_date_f.close()
            if(len(date.split(":")) == 2):
               return date.split(":")[1]
            else:
               return "0" 
        else:
            return "0" #No Version


if __name__ =='__main__':
    app.run(host='0.0.0.0',port=2001,debug=True)
