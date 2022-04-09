import cv2
from flask import render_template, request, url_for, session, jsonify
from flask_login.utils import login_required
from flask_login import current_user, login_user
from sqlalchemy.sql.functions import user
from __init__ import app
import json

from models import PictureModel
from src.python.service.Service import AuthService, PictureService, ShareService

import img_enc_dec as imgEnDe

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

import base64
import urllib

picSer = PictureService()
shareSer = ShareService()
auSer = AuthService()

import os
def savePic(image_64_encode,user_id,file_name):
    try:
        os.makedirs("static/uploads/"+str(user_id))
    except FileExistsError:
        print('exist')
    resource = urllib.request.urlopen(image_64_encode)
    file_name = 'static/uploads/'+file_name #trong file_name la "userid/pic.png"
    with open(file_name,"wb") as output:
        output.write(resource.read())
        
        output.close()
        

    imgEnDe.encrypt(file_name)
        
        

@app.route("/mypicture/upload_img",methods=["POST"])
@login_required
def upload_img():
    user_id = current_user.id
    data = request.get_json(force=True)
    image_64_encode= data['readfile']
    file_name=  data['name']
    pic = picSer.insert(user_id,file_name) 
    if(pic):
        savePic(image_64_encode,user_id,pic.pic) #trong pic.pic la "userid/pic.png"
        res= True
    else:
        res = False
    res = {
        'success': res
    }
    return json.dumps(res)

@login_required
@app.route("/mypicture/getPictures",methods=["GET"])
def getPictures():
    user_id = current_user.id
    pics = picSer.getByUserID(user_id)    
    pictures = [{'picture_id':i.id}.copy() for i in pics]
    map={
        "userlogin_id":current_user.id,
        "picture_ids":pictures
    }
    return json.dumps(map)

from base64 import b64encode, decode # or urlsafe_b64decode

from urllib.error import URLError, HTTPError
import flask

@login_required
@app.route("/mypicture/searchPicture/<int:picture_id>",methods=["GET"])
def searchPicture(picture_id):
    user_id = current_user.id
    pic = picSer.searchByPicID(user_id,picture_id)
    if(pic==None): return ""

    url_img =  'static/uploads/' +pic.pic
    
    try:
        imgInput = cv2.imread(url_img)
        decode = imgEnDe.decrypt(imgInput)
        #convert img data to bytes
        is_success, im_buf_arr = cv2.imencode(".png", decode)
        byte_im = im_buf_arr.tobytes()
        
        #convert byte to data urls
        b64_mystring = b64encode(byte_im).decode("utf-8")
        url_img ="data:image/png;base64,"+b64_mystring
        fin = open("test.txt","w+")
        fin.write(str(decode))
        fin.close()
    except HTTPError as e:
        print('Error code: ', e.code)
    except URLError as e:
        print('Reason: ', e.reason)

    


    
    map={
        "picture_id": pic.id,
        "create_at": str(pic.create_at),
        "pic": url_img,
        "userlogin_id":pic.userlogin_id,
        "fullname": pic.userlogin.fullname,
        "username": pic.userlogin.username
    }
    return json.dumps(map,default=str)


#list cac picture duoc shaare cho usser
@login_required
@app.route("/sharepicture/getShare",methods=["GET"])
def getPictureShared():
    user_id = current_user.id
    shares = shareSer.getByUserID(user_id)    
    pictures = [{ 'picture_id':i.picture_id, }.copy()  for i in shares]
    map={
        "userlogin_id":current_user.id,
        "picture_ids":pictures
    }
    return json.dumps(map)


@login_required
@app.route("/sharepicture/shareFor/<int:picture_id>",methods=["GET"])
def listShareFor(picture_id):
    user_id = current_user.id
    if not picSer.is_Permission(user_id,picture_id): return ""
    shares = shareSer.searchByPicID(picture_id)    
    userAvail = shareSer.searchAvailableUser(picture_id)
    list_share = [{'userlogin_id':sh.userlogin_id,}.copy() for sh in shares ]  #danh sach user da share
    list_avail = [{'userlogin_id':u.id}.copy() for u in userAvail]     #danh sach user chua duoc share
    
    map={
        "userlogin_id":user_id,
        "picture_id":picture_id,
        "share_user_id":list_share,
        "available_user_id":list_avail
    }
    return json.dumps(map)

#@login_required
@app.route("/sharepicture/shareTo",methods=["POST","DELETE"])
def shareTo():
    user_id = current_user.id
    data = request.get_json(force=True)
    picture_id= data['picture_id']
    username = data['username']
    user = auSer.getByUsername(username)
    if(not user):
        res=False
        mess="Username không tồn tại"
    
    elif(not picSer.is_Permission(user_id,picture_id)):
        res=False
        mess="Bạn không có quyền chia sẽ"
    else:  
        if(request.method=="POST"):
            res = not not shareSer.insert(picture_id,user.id)
            mess = "Chia sẽ thành công" if res else "Đã chia sẽ"
        else:
            res = not not shareSer.remove(picture_id,user.id)
            mess = "Xoá thành công" if res else "Lỗi xoá"

    map={
        "success":res,
        "message": mess
    }
    return json.dumps(map)



