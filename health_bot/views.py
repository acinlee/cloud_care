from django.shortcuts import render, redirect, render_to_response
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.utils import timezone
import json, random, string
from django.http import JsonResponse
from .forms import *
from PIL import Image
from datetime import datetime
#오류 알림 메세지
from django.contrib import messages
#이메일 관련 import
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import AccountActivationTokenGenerator
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
import itertools
#android
from rest_framework import viewsets
from health_bot.serializers import UserSerializer

#csv
import csv

#opencv
import cv2 as cv
import numpy as np
import pytesseract
from pytesseract import *
import re
import urllib.request
import urllib.parse as parse
from urllib.parse import quote
import xmltodict
import requests


# Create your views here.
ServiceKey="qjxP80L1gooQePXFXKhFd%2BXwiKxAyipUx1phE%2F6JZ9iQwqhD8EUTiXO8244ROcnVAbOHU8pc7xueCGGe9j0dcQ%3D%3D"
#배열 해제
def from_iterable(iterables):
    # chain.from_iterable(['ABC', 'DEF']) --> ['A', 'B', 'C', 'D', 'E', 'F']
    for it in iterables:
        for element in it:
            yield element

#메인 화면
def main_page(request):
    user = User.objects.get(user_email=request.session['user_email'])
    try:
        family_list = User.objects.filter(family_name = user.family_name).exclude(family_name__isnull=True)
        prescription_list = Prescription.objects.filter(prescription_user=user)
        data={}
        for prescription_object in prescription_list:
            disease_object = Disease.objects.get(disease_prescription=prescription_object.id)
            data.setdefault(prescription_object, disease_object)
        return render(request, 'health_bot/main/main_function.html', {'user' : user, 'family_list':family_list, 'data':data})
    except: 
        return render(request, 'health_bot/main/main_function.html', {'user' : user,})

#질병별
def disease_main_page(request, family_id):
    #user = User.objects.get(user_email=request.session['user_email'])
    user = User.objects.get(pk=family_id)
    disease_color = "1" #질병별인지
    try:
        family_list = User.objects.filter(family_name = user.family_name).exclude(family_name__isnull=True)
        prescription_list = Prescription.objects.filter(prescription_user=user)
        disease_list = []
        for prescription_object in prescription_list:
            disease_list.append(Disease.objects.filter(disease_prescription=prescription_object).order_by('disease_name'))
        disease_list_fi = list(itertools.chain.from_iterable(disease_list))
        data={}
        for disease_object in disease_list_fi:
            prescription_object = Prescription.objects.get(id=disease_object.disease_prescription.id)
            data.setdefault(prescription_object, disease_object)

        return render(request, 'health_bot/main/main_function.html', {'user' : user, 'family_list':family_list, 'data':data, 'disease_color':disease_color})
    except: 
        return render(request, 'health_bot/main/main_function.html', {'user' : user,})

#진료일별
def hos_main_page(request, family_id):
    #user = User.objects.get(user_email=request.session['user_email'])
    user = User.objects.get(pk=family_id)
    hos_color = "1" #진료일별인지
    try:
        family_list = User.objects.filter(family_name = user.family_name).exclude(family_name__isnull=True)
        prescription_list = Prescription.objects.filter(prescription_user=user).order_by('prescription_date')
        data={}
        for prescription_object in prescription_list:
            disease_object = Disease.objects.get(disease_prescription=prescription_object.id)
            data.setdefault(prescription_object, disease_object)
        return render(request, 'health_bot/main/main_function.html', {'user' : user, 'family_list':family_list, 'data':data, 'hos_color':hos_color})
    except: 
        return render(request, 'health_bot/main/main_function.html', {'user' : user,})


#세션 관리
#1. 세션 추가
def addSessions(request, user):
    request.session['user_email'] = user.user_email
    request.session['user_pw'] = user.user_pw
    
#2. 세션 제거
def Logout(request):
    for item in list(request.session.keys()):
        del request.session[item]
    return render(request, 'health_bot/login/login.html')    

#3. 접속 유저 관리
def getUser(request):
    user = User.objects.get(user_email=request.session['user_email'])
    return user
    
#로고 화면
def First(request):
    return render(request, 'health_bot/first_view.html')

#회원 관련
#1. 로그인 화면
def Login_view(request):
    return render(request, 'health_bot/login/login.html')

#2. 로그인 기능
def Login(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']
        try:
            user = User.objects.get(user_email=user_email)
            if user_pw == user.user_pw:
                addSessions(request, user)
                try:
                    family_list = User.objects.filter(family_name = user.family_name).exclude(family_name__isnull=True)
                    prescription_list = Prescription.objects.filter(prescription_user=user)
                    data={}
                    for prescription_object in prescription_list:
                        disease_object = Disease.objects.get(disease_prescription=prescription_object.id)
                        data.setdefault(prescription_object, disease_object)

                    messages.info(request, '로그인 성공')    
                    return render(request, 'health_bot/main/main_function.html', {
                        'user' : user, 'family_list':family_list, 'data':data})
                except:
                    messages.info(request, '로그인 성공')    
                    return render(request, 'health_bot/main/main_function.html', {
                        'user' : user,})
            elif user_pw != user.user_pw:
                return render_to_response('health_bot/statementpage/Error.html', {
                    'alert_msg' : '비밀번호가 맞지 않습니다.',
                    'url' : '/'
                })
        except User.DoesNotExist:
            return render_to_response('health_bot/statementpage/Error.html', {
                    'alert_msg' : '해당 아이디가 없습니다.',
                    'url' : '/'
                })
    else:
        return render(request, 'health_bot/login/login.html')

#3. 회원가입 화면 이동
def Signup_view(request):
    return render(request, 'health_bot/login/signup.html')

#4. 회원 가입
def SignUp(request):
    if request.method == "POST":
        try:
            pw_ok=request.POST['user_pw_ok']
            pw=request.POST['user_pw']
            UserList = User.objects.filter(user_email=request.POST['user_email'])
            if UserList:
                messages.info(request, '중복된 이메일입니다')
                return render(request, 'health_bot/login/signup.html')
            if pw_ok != pw:
                messages.info(request, '비밀번호를 다시 확인해 주세요')
                return render(request, 'health_bot/login/signup.html')    
            #성별
            gendercheck = request.POST['user_gender']
            
            user = User.objects.create(
            user_email = request.POST['user_email'],
            user_pw = request.POST['user_pw'],
            user_name = request.POST['user_name'],
            user_sex = gendercheck,
            user_age = request.POST['user_age'],
            )
            messages.info(request, '회원가입이 완료되었습니다.')
            return render(request, 'health_bot/login/login.html')
        except:
            messages.error(request, '양식 오류')
            return render(request, 'health_bot/login/signup.html')

    return render(request, 'health_bot/statementpage/Error.html')

#5. 비밀번호 초기화 이동
def Pw_reset_view(request):
    return render(request, 'health_bot/user_find/pw_reset.html')

#6. 비밀번호 초기화
def Pw_reset(request):
    try:
        user = User.objects.get(user_email=request.POST['user_email'])
        _LENGTH = 12 # 12자리
        # 숫자 + 대소문자
        string_pool = string.ascii_letters + string.digits
        # 랜덤한 문자열 생성
        update_usr_pw = "" 
        for i in range(_LENGTH) :
            update_usr_pw += random.choice(string_pool) # 랜덤한 문자열 하나 선택
        User.objects.filter(user_email=request.POST['user_email']).update(
            user_pw = update_usr_pw,
        )
        message = render_to_string('health_bot/user_find/pw_reset_email.html', {
            'user_pw':update_usr_pw,
        })
        mail_subject = "[CloudCare] 임시 비밀번호 메일입니다."
        user_email = user.user_email
        email = EmailMessage(mail_subject, message, to=[user_email])
        email.send()
        messages.info(request, '초기 비밀번호 발송이 완료되었습니다.')
        return render(request, 'health_bot/login/login.html')
    except:
        messages.error(request, '해당하는 정보의 회원이 없습니다.')
        return redirect('health_bot:pw_reset_view')

#7.마이페이지
def mypage(request):
    user = User.objects.get(user_email=request.session['user_email'])
    return render(request, 'health_bot/mypage/mypage.html', {'user': user})

#8.사용자 정보 수정 이동
def user_edit_go(request):
    user = User.objects.get(user_email=request.session['user_email'])
    return render(request, 'health_bot/mypage/mypage_edit.html', {'user': user})

#9.사용자 정보 수정
def user_edit(request):
    if request.method == "POST":
        user = User.objects.get(user_email=request.session['user_email'])
        try:
            user_img = request.FILES.get('user_img')
            user.user_photo = user_img
            user.save()
        except:
            pass
        if request.POST['new_name'] != "":
            new_name = request.POST['new_name']
        else:
            new_name = user.user_name

        if request.POST['new_pw_check'] == "" and request.POST['new_pw'] =="":
            pw = user.user_pw 
        elif request.POST['new_pw_check'] != "" and request.POST['new_pw'] =="":
            messages.error(request, '비밀번호 입력 오류')
            return render(request, 'health_bot/mypage/mypage_edit.html', {'user': user})
        elif request.POST['new_pw_check'] == "" and request.POST['new_pw'] !="":
            messages.error(request, '비밀번호 확인 오류')
            return render(request, 'health_bot/mypage/mypage_edit.html', {'user': user})
        else:
            pw = request.POST['new_pw_check']
            pw_check = request.POST['new_pw']
            if pw_check != pw:
                messages.error(request, '비밀번호 불일치')
                return render(request, 'health_bot/mypage/mypage_edit.html', {'user': user})
        
        User.objects.filter(user_email=user.user_email).update(
            user_name = new_name,
            user_pw = pw,
        )
        try:
            family_list = User.objects.filter(family_name = user.family_name)
            messages.info(request, "수정 완료")
            return render(request, 'health_bot/main/main_function.html', {'user' : user, 'family_list':family_list,})
        except:
            messages.info(request, "수정 완료") 
            return render(request, 'health_bot/main/main_function.html', {'user' : user,})

#10.사용자 사진 변경
def user_photo_edit(request):
    if request.method == "POST":
        user = User.objects.get(user_email=request.session['user_email'])
        try:
            User.objects.filter(user_email=user.user_email).update(
                user_photo = request.FILES['user_photo_edit'],
            )
            messages.info(request, "프로필 사진 변경 완료")
            return render(request, 'health_bot/mypage/mypage.html', {'user': user})
        except:
            messages.error(request, "파일을 다시 선택해 주세요")
            return render(request, 'health_bot/mypage/mypage_edit.html', {'user': user})

#메인 기능
#1.가족 추가페이지 이동
def family_create_page(request):
    user = User.objects.get(user_email=request.session['user_email'])
    if user.family_name:
        messages.error(request, "이미 가족 구성원입니다.")
        return render(request, 'health_bot/mypage/mypage.html', {'user': user})
    else:
        return render(request, 'health_bot/family/family_create.html', {'user':user})

#2.가족 이름 설정
def family_create(request):
    if request.method == "POST":
        user = User.objects.get(user_email=request.session['user_email'])
        if request.POST['family_name']=="":
            messages.error(request, "가족 이름을 설정해 주세요")
            return render(request, 'health_bot/family/family_create.html', {'user':user})
        else:
            family = Family.objects.create(
                family_name = request.POST['family_name'],
            )
            User.objects.filter(user_email=request.session['user_email']).update(
                family_name =family.pk
            )
            return render(request, 'health_bot/family/family_add_user.html', {'user':user, 'family':family})
            
#3.유저 찾기
def userFind(request):
    user_email = request.POST['user_email'] #유저가 입력한 텍스트
    user_list = User.objects.filter(user_email__icontains=user_email).exclude(user_email=request.session['user_email']).exclude(family_name__isnull=False).order_by('user_email')
    user_id_list = []
    for user in user_list:
        user_id_list.append(user.pk)
    
    if not user_id_list:
        context = {  'msg' : 'N',  }
    else:
        context = {  'msg' : 'Y', 'user_id_list':user_id_list,}

    return HttpResponse(json.dumps(context), content_type="application/json")

#4.유저 추가
def userAdd(request):
    user_id = request.POST['user_id'] #유저가 입력한 텍스트
    user = User.objects.get(user_email=request.session['user_email'])
    User.objects.filter(user_email=user_id).update(
        family_name = user.family_name
    )
    return HttpResponse("success")

#5.유저 삭제
def userDelete(request):
    friend_id = request.POST['friend_id']
    user = User.objects.get(DanTalk_ID=request.session['dantalk_id'])
    FriendList.objects.get(Have_Friend_User=user, Friend_ID=friend_id).delete()

    return HttpResponse("success")

#6.가족 구성원 추가 페이지 이동
def family_memeber_add_page(request):
    user = User.objects.get(user_email=request.session['user_email'])
    try:
        family = Family.objects.filter(pk=user.family_name.pk)
        return render(request, 'health_bot/family/family_add_user.html', {'user':user, 'family':family})

    except:
        messages.error(request, '가족을 먼저 생성해 주세요')
        return redirect('health_bot:mypage')
    

#7.처방전 사진 촬영
def opencv_prescription(request):   
    user = User.objects.get(user_email=request.session['user_email'])
    if request.method == 'POST': # method가 POST 방식이라면 글이 써진 것
        
        pre = Prescription.objects.create(
            prescription_user = user,
            prescription_date = timezone.now(),
            prescription_photo = request.FILES['camera']
        )
        imgpre_1 = cv.imread('C:/Users/acin3/Downloads/test/test5.jpg')#cv.imread("./media/"+str(pre.prescription_photo))

        pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

        img = cv.resize(imgpre_1, dsize=(720, 720), interpolation=cv.INTER_AREA) #리사이즈 이미지
        dst = img.copy()
        disease = dst[180:220, 67:190] #질병코드
        #md1 = img[250:300, 30:314] #약코드1
        md1 = dst[280:315, 20:314] #약코드1
        #md3 = dst[316:332, 30:314] #약코드3
        md2 = dst[315:350, 20:314] #약코드2
        #md5 = dst[351:366, 30:314] #약코드5
        md3 = dst[350:385, 20:314] #약코드3
        #md7 = dst[386:405, 30:314] #약코드7
        md4 = dst[390:420, 20:314] #약코드4
        #md9 = dst[421:440, 30:314] #약코드9
        md5 = dst[421:455, 20:314] #약코드5
        #md11 = dst[455:470, 30:314] #약코드11
        md6 = dst[455:488, 20:314] #약코드6
        #md13 = dst[489:505, 30:314] #약코드13
        md7 = dst[490:522, 20:314] #약코드7
        #md15 = dst[523:540, 30:314] #약코드15
        md8 = dst[523:555, 20:314] #약코드8

        # cv.namedWindow('image')
        # while(True):
        #     cv.imshow('disease', disease)
        #     cv.imshow('md1', md1)
        #     cv.imshow('md2', md2)
        #     cv.imshow('md3', md3)
        #     cv.imshow('md4', md4)
        #     cv.imshow('md5', md5)
        #     cv.imshow('md6', md6)
        #     cv.imshow('md7', md7)
        #     cv.imshow('md8', md8)
        #     cv.imshow('md9', md9)
        #     cv.imshow('md10', md10)
        #     cv.imshow('md11', md11)
        #     cv.imshow('md12', md12)
        #     cv.imshow('md13', md13)
        #     cv.imshow('md14', md14)
        #     cv.imshow('md15', md15)
        #     cv.imshow('md16', md16)

        #     k=cv.waitKey(1) & 0xFF
        #     if k==27:
        #         print('종료')
        #         break
        # cv.destroyAllWindows()
        md_list = [md1,md2,md3,md4,md5,md6,md7,md8]
        di_code_fi = pytesseract.image_to_string(disease, lang='fra') #질병 코드
        md_code_list = []
        for med in md_list:
            md_code_before = pytesseract.image_to_string(med, lang='eng+kor')
            md_code_fi = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', md_code_before.split(' ')[0])
            if md_code_fi==" " or md_code_fi=="":
                break
            else:
                print(md_code_fi)
                md_code_list.append(md_code_fi) #약 코드

        return render(request, 'health_bot/prescription_pic/user_prescription_confirm.html', {'di_code_fi':di_code_fi, 'md_code_list':md_code_list, 'prescription':pre})

#8.처방전 사용자가 정보 확인 후 db에 처방전 정보 저장
def prescription_confirm(request):
    from bs4 import BeautifulSoup
    if request.method == 'POST':
        md_code = request.POST.getlist('md_code') #의약품 코드 리스트
        print(md_code)
        di_code = request.POST['di_code'] #질병 코드

        url_di = 'http://apis.data.go.kr/B551182/diseaseInfoService/getDissNameCodeList?sickType=1&medTp=2&diseaseType=SICK_CD&searchText='+di_code+'&ServiceKey=qjxP80L1gooQePXFXKhFd%2BXwiKxAyipUx1phE%2F6JZ9iQwqhD8EUTiXO8244ROcnVAbOHU8pc7xueCGGe9j0dcQ%3D%3D&_type=json'
        req = requests.get(url_di)
        req_json_dumps = json.loads(req.text)
        sick_name = req_json_dumps['response']['body']['items']['item']['sickNm'] #병명
        sick_code = req_json_dumps['response']['body']['items']['item']['sickCd'] #병코드

        pre_foreign = Prescription.objects.get(pk=request.POST['pre_info']) #처방전 id
        Disease.objects.create(
            disease_prescription = pre_foreign,
            disease_name = sick_name,
            disease_code = sick_code
        ) #질병 정보 저장
        for medicine_code in md_code:
            if medicine_code == "" or medicine_code == " ":
                pass
            else:
                url='http://apis.data.go.kr/1470000/MdcinGrnIdntfcInfoService/getMdcinGrnIdntfcInfoList?ServiceKey=qjxP80L1gooQePXFXKhFd%2BXwiKxAyipUx1phE%2F6JZ9iQwqhD8EUTiXO8244ROcnVAbOHU8pc7xueCGGe9j0dcQ%3D%3D&numOfRows=3&pageNo=1&edi_code='+medicine_code
                response = urllib.request.urlopen(url)
                json_str = response.read().decode("utf-8")
                string = json_str[json_str.find('<item>'):json_str.find('</item>')+7]
                
                soup = BeautifulSoup(string, 'html.parser')
                text = None              
                for tag in soup:
                    text = tag.text.split('\n')
                    text = text[1:len(text)-1]
                if text is None:
                    continue
                Medicine.objects.create(
                    pre_medicine = pre_foreign,
                    item_seq = text[0],#품목일련번호
                    item_name = text[1], #품목명
                    entp_seb = text[2], #업체일련번호
                    entp_name = text[3], #업체명
                    chart = text[4], #성상
                    item_image = text[5], #큰제품이미지
                    print_pront = text[6], #표시(앞)
                    print_back = text[7], #표시(뒤)
                    drug_shape = text[8], #의약품모양
                    color_front = text[9], #색깔(앞)
                    color_back = text[10], #색깔(뒤)
                    line_front = text[11], #분할선(앞)
                    line_back = text[12], #분할선(뒤)
                    leng_long = text[13], #크기(장축)
                    leng_short = text[14], #크기(단축)
                    thick = text[15], #크기(두께)
                    img_regist_ts = text[16], #약학정보원 이미지 생성일
                    class_no = text[17], #분류번호
                    class_name = text[18], #분류명
                    etc_otc_name = text[19], #전문/일반
                    item_permit_date = text[20], #품목허가일자
                    form_code_name = text[21], #체형코드이름
                    mark_code_front_anal = text[22], #마크내용(앞)
                    mark_code_back_anal = text[23], #마크내용(뒤)
                    mark_code_front_img = text[24], #마크이미지(앞)
                    mark_code_back_img = text[25], #마크이미지(뒤)
                    item_eng_name = text[26], #제품 영문명
                    change_date = text[27], #변경일자
                    mark_code_front = text[28], #마크코드(앞)
                    mark_code_back = text[29], #마크코드(뒤)
                    edi_code = text[30] #보험코드
                )
                print('hello')

        medicine = Medicine.objects.filter(pre_medicine=pre_foreign)
        #병용금기    
        for overlap in medicine:
            item_name = quote(overlap.item_name.split('(')[0])
            url='http://apis.data.go.kr/1470000/DURPrdlstInfoService/getUsjntTabooInfoList?ServiceKey=qjxP80L1gooQePXFXKhFd%2BXwiKxAyipUx1phE%2F6JZ9iQwqhD8EUTiXO8244ROcnVAbOHU8pc7xueCGGe9j0dcQ%3D%3D&itemName='+item_name+'&numOfRows=1&pageNo=1'
            response = urllib.request.urlopen(url)
            json_str = response.read().decode("utf-8")
            jsonString = json.dumps(xmltodict.parse(json_str), indent=4)
            req_json_dumps = json.loads(jsonString)
            if req_json_dumps['response']['body']['totalCount'] == "0":
                pass
            else:
                OpenOverBan.objects.create(
                    over_medicine = overlap,
                    ingr_code = req_json_dumps['response']['body']['items']['item']['INGR_CODE'],
                    ingr_kor_name = req_json_dumps['response']['body']['items']['item']['INGR_KOR_NAME'],
                    ingr_eng_name = req_json_dumps['response']['body']['items']['item']['INGR_ENG_NAME'],
                    item_seq = req_json_dumps['response']['body']['items']['item']['ITEM_SEQ'],
                    item_name = req_json_dumps['response']['body']['items']['item']['ITEM_NAME'],
                    mixture_ingr_code = req_json_dumps['response']['body']['items']['item']['MIXTURE_INGR_CODE'],
                    mixture_ingr_kor_name = req_json_dumps['response']['body']['items']['item']['MIXTURE_INGR_KOR_NAME'],
                    mixture_ingr_eng_name = req_json_dumps['response']['body']['items']['item']['MIXTURE_INGR_ENG_NAME'],
                    mixture_item_seq = req_json_dumps['response']['body']['items']['item']['MIXTURE_ITEM_SEQ'],
                    mixture_item_name = req_json_dumps['response']['body']['items']['item']['MIXTURE_ITEM_NAME'],
                    mixture_class_name = req_json_dumps['response']['body']['items']['item']['MIXTURE_CLASS_NAME'],
                    prohbt_content = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', req_json_dumps['response']['body']['items']['item']['PROHBT_CONTENT'])
                )

        #임부금기
        for pregnat in medicine:
            #품목 정보 api
            item_name = quote(pregnat.item_name.split('(')[0])
            url1='http://apis.data.go.kr/1470000/DURPrdlstInfoService/getPwnmTabooInfoList?ServiceKey=qjxP80L1gooQePXFXKhFd%2BXwiKxAyipUx1phE%2F6JZ9iQwqhD8EUTiXO8244ROcnVAbOHU8pc7xueCGGe9j0dcQ%3D%3D&itemName='+item_name+'&numOfRows=1&pageNo=1'
            response = urllib.request.urlopen(url1)
            json_str = response.read().decode("utf-8")
            jsonString = json.dumps(xmltodict.parse(json_str), indent=4)
            req_json_dumps = json.loads(jsonString)
            #성분 정보 api - 여기서는 임부금기 등급만 가져옴
            try:
                ingrCode=req_json_dumps['response']['body']['items']['item']['INGR_CODE']
                url2='http://apis.data.go.kr/1470000/DURIrdntInfoService/getPwnmTabooInfoList?ServiceKey=qjxP80L1gooQePXFXKhFd%2BXwiKxAyipUx1phE%2F6JZ9iQwqhD8EUTiXO8244ROcnVAbOHU8pc7xueCGGe9j0dcQ%3D%3D&ingrCode='+ingrCode+'&numOfRows=3&pageNo=1'
                response2 = urllib.request.urlopen(url2)
                json_str2 = response2.read().decode("utf-8")
                jsonString2 = json.dumps(xmltodict.parse(json_str2), indent=4)
                req_json_dumps2 = json.loads(jsonString2)
                if req_json_dumps['response']['body']['totalCount'] == "0" and req_json_dumps2['response']['body']['totalCount'] == "0":
                    pass
                else:
                    OpenPregnatBan.objects.create(
                        pregnat_medicine = pregnat,
                        ingr_code = req_json_dumps['response']['body']['items']['item']['INGR_CODE'],
                        ingr_kor_name = req_json_dumps['response']['body']['items']['item']['INGR_NAME'],
                        ingr_eng_name = req_json_dumps['response']['body']['items']['item']['INGR_ENG_NAME'],
                        item_seq = req_json_dumps['response']['body']['items']['item']['ITEM_SEQ'],
                        item_name = req_json_dumps['response']['body']['items']['item']['ITEM_NAME'],
                        grade = req_json_dumps2['response']['body']['items']['item']['GRADE'],
                        prohbt_content = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', req_json_dumps['response']['body']['items']['item']['PROHBT_CONTENT'])
                    )
            except:
                pass

        #효능군 중복
        for efficacy in medicine:
            item_name = quote(efficacy.item_name.split('(')[0])
            url='http://apis.data.go.kr/1470000/DURPrdlstInfoService/getEfcyDplctInfoList?ServiceKey=qjxP80L1gooQePXFXKhFd%2BXwiKxAyipUx1phE%2F6JZ9iQwqhD8EUTiXO8244ROcnVAbOHU8pc7xueCGGe9j0dcQ%3D%3D&itemName='+item_name+'&numOfRows=1&pageNo=1'
            response = urllib.request.urlopen(url)
            json_str = response.read().decode("utf-8")
            jsonString = json.dumps(xmltodict.parse(json_str), indent=4)
            req_json_dumps = json.loads(jsonString)
            if req_json_dumps['response']['body']['totalCount'] == "0":
                pass
            else:
                OpenEfficacyGroupOverlap.objects.create(
                    efficacy_medicine = efficacy,
                    ingr_code = req_json_dumps['response']['body']['items']['item']['INGR_CODE'],
                    item_seq = req_json_dumps['response']['body']['items']['item']['ITEM_SEQ'],
                    item_name = req_json_dumps['response']['body']['items']['item']['ITEM_NAME']
                )
        return redirect('health_bot:main_page')

#9. 처방전 사진 취소시 처방전 정보 삭제
def prescription_cancel(request, pre_info):
    Prescription.objects.get(id=pre_info).delete()
    return redirect('health_bot:main_page')

#10. 처방전 상세 정보
def prescription_detail_info(request, pre_info):
    prescription = Prescription.objects.get(pk=pre_info)
    disease = Disease.objects.get(disease_prescription=pre_info)
    medicine = Medicine.objects.filter(pre_medicine=pre_info)
    return render(request, 'health_bot/prescription_detail_info/prescription_detail.html', {'prescription':prescription ,'disease':disease, 'medicine':medicine})

#11. 의약품 상세 정보
def medicine_detail_info(request, medicine_info):
    medicine_info = Medicine.objects.get(id=medicine_info)
    year = medicine_info.item_permit_date[0:4]
    month = medicine_info.item_permit_date[4:6]
    day = medicine_info.item_permit_date[6:8]
    return render(request, 'health_bot/prescription_detail_info/medicine_info.html', {'medicine':medicine_info, 'year':year, 'month':month, 'day':day})

#12. 가족 처방전 확인
def family_prescription_check(request, family_id):
    user = User.objects.get(pk=family_id)
    try:
        family_list = User.objects.filter(family_name = user.family_name).exclude(family_name__isnull=True)
        prescription_list = Prescription.objects.filter(prescription_user=user)
        data={}
        for prescription_object in prescription_list:
            disease_object = Disease.objects.get(disease_prescription=prescription_object.id)
            data.setdefault(prescription_object, disease_object)
        return render(request, 'health_bot/main/main_function.html', {'user' : user, 'family_list':family_list, 'data':data})
    except: 
        return render(request, 'health_bot/main/main_function.html', {'user' : user,})

#django android test
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#android signup
def app_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email_content', '')
        pw = request.POST.get('pw_content', '')
        try:
            user = User.objects.get(user_email=email)
            if pw == user.user_pw:
                addSessions(request, user)
                return JsonResponse({'code' : '0000', 'msg' : '로그인 성공'})
            elif pw != user.al_PW:
                return JsonResponse({'code' : '0001', 'msg' : '비밀번호 오류'})
        except User.DoesNotExist:
            return JsonResponse({'code' : '0011', 'msg' : '존재하지 않는 아이디'})

