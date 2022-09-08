# -*- coding: utf-8 -*-
import threading
import os
import signal
from os_ import getFiles, getFile_,getConfig
import sys
from flask import Flask, render_template
from flask import request
from flask_cors import CORS, cross_origin
import json
import socket
from waitress import serve
from werkzeug.utils import secure_filename 

def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

IP=getIp()

TEMPLATES_AUTO_RELOAD = True

class JSON:
    def __init__(self):
        self.json = "JSON"
    def string(self,dic):
        return json.dumps(dic, separators=(',', ':'))
    def parse(self,string):
        return json.loads(string)

JSON = JSON()

try:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
except:
    HOST = IP
    PORT = 789

UPLOAD_FOLDER = './temp'
static_folder = 'null'
try:
    static_folder = os.path.join(sys._MEIPASS, 'static')
except:
    static_folder = './static'

class WebService:
    def __init__(self):
        
        if getattr(sys, 'frozen', False):
            template_folder = os.path.join(sys._MEIPASS, 'template')
            static_folder = os.path.join(sys._MEIPASS, 'static')
            self.app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)
        else:
            self.app = Flask(__name__,template_folder='template',static_folder='static')

        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

        @self.app.route('/')
        @cross_origin(supports_credentials=True)
        def index():
            return render_template('./index.html')
        
        @self.app.route('/get', methods = ['POST'])
        @cross_origin(supports_credentials=True)
        def get():
            try:
                data = request.json
            except:
                return {"status":False,"mensage":"Dados (JSON) ausentes, Method Post"}
            if(not data['path']):
                return {'status':False,'mensagem':'Caminho não específicado !'}
            return getFiles(data['path'])

        @self.app.route('/getFile', methods = ['POST'])
        @cross_origin(supports_credentials=True)
        def getFile():
            try:
                data = request.json
            except:
                return {"status":False,"mensage":"Dados (JSON) ausentes, Method Post"}
            return getFile_(data['path'])
        
        @self.app.route('/sendFile', methods = ['POST'])
        @cross_origin(supports_credentials=True)
        def sendFile():
            try:
                data = request.files
            except:
                return {"status":False,"mensage":"Dados (JSON) ausentes, Method Post"}
            path = request.form['path']
            for file in data:
                uploaded_file = data.get(file)  
                uploaded_file.filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(path,uploaded_file.filename)) 
            return {'status':True}

    def run(self):
        extra_dirs = ['./']
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)
        public, config, port = getConfig(HOST,PORT)
        page = open('{}/config.js'.format(static_folder),'w')
        page.write(config)
        page.close()
        if(public):
            print(" \n[*] - Servidor iniciado de maneira pública !")
        print(" \n[*] - Servidor iniciado - {}:{}".format(HOST if not public else '127.0.0.1',port))
        serve(self.app,host=HOST if not public else '127.0.0.1', port=port)
    

def main():
    while True:
        try:
            kill=input()
            if(kill=='cls'):
                os.system('clear')
                print("\n\033[1;35m[*] On: {} - {}\033[0;0m\n".format(HOST,PORT))
        except KeyboardInterrupt:
            os.kill(os.getpid(),signal.SIGKILL)

try:
    thread = threading.Thread(target=main)
    thread.start()
    web_service = WebService()
    web_service.run()

except KeyboardInterrupt:
    os.kill(os.getpid(),signal.SIGKILL)
