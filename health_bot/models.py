from django.db import models

# Create your models here.
class User(models.Model):
    class meta:
        db_table = '사용자 속성'
    user_email = models.CharField(primary_key=True, max_length=30)
    user_name = models.CharField(max_length=5, null=False)
    user_age = models.IntegerField(null=False) 
    user_sex = models.BooleanField(default=True)
    user_pw = models.CharField(null=False, max_length=15)
    user_photo = models.FileField(blank=True)

class Notification(models.Model):
    class meta:
        db_table = '알림'
    #로그인한 유저    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    #친구추가한 유저
    family_user = models.ForeignKey(User,related_name='noti_family_user', on_delete=models.CASCADE, null=True, blank=True) 
    family_id = models.IntegerField()


class Family(models.Model):
    class meta:
        db_table = '가족 구성'
    family_name = models.CharField(max_length=10)  
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)

class FamilyList(models.Model):
    class meta:
        db_table = '가족 목록'
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    family_user = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="family_user",null=True, blank=True)
    family = models.ForeignKey(Family, on_delete=models.DO_NOTHING, null=True, blank=True)      

class Prescription(models.Model):
    class meta:
        db_table = '처방전'
    prescription_user = models.ForeignKey(User, on_delete=models.CASCADE)
    prescription_date = models.DateTimeField(null=True, blank=False)
    prescription_photo = models.FileField(blank=True)
    hospital_name = models.CharField(null=True, max_length=30)
    hospital_web = models.CharField(null=True, blank=True, max_length=50)

class Disease(models.Model):
    class meta:
        db_table = '질병명'
    disease_prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True, related_name='disease')
    disease_name = models.CharField(null=True, blank=True, max_length=30)
    disease_code = models.CharField(null=True, blank=True, max_length=30)

class Medicine(models.Model):
    class meta:
        db_table = '약 정보 저장'
    pre_medicine = models.ForeignKey(Prescription, on_delete=models.CASCADE, null=True)
    item_seq = models.CharField(null=True, blank=True, max_length=30)#품목일련번호
    item_name = models.CharField(null=True, blank=True, max_length=30)#품목명
    entp_seb = models.CharField(null=True, blank=True, max_length=30)#업체일련번호
    entp_name = models.CharField(null=True, blank=True, max_length=30) #업체명
    chart = models.CharField(null=True, blank=True, max_length=30)#성상
    item_image = models.CharField(null=True, blank=True, max_length=100)#큰제품이미지
    print_pront = models.CharField(null=True, blank=True, max_length=30)#표시(앞)
    print_back = models.CharField(null=True, blank=True, max_length=30)#표시(뒤)
    drug_shape = models.CharField(null=True, blank=True, max_length=30)#의약품모양
    color_front = models.CharField(null=True, blank=True, max_length=30)#색깔(앞)
    color_back = models.CharField(null=True, blank=True, max_length=30)#색깔(뒤)
    line_front = models.CharField(null=True, blank=True, max_length=30)#분할선(앞)
    line_back = models.CharField(null=True, blank=True, max_length=30)#분할선(뒤)
    leng_long = models.CharField(null=True, blank=True, max_length=30)#크기(장축)
    leng_short = models.CharField(null=True, blank=True, max_length=30)#크기(단축)
    thick = models.CharField(null=True, blank=True, max_length=30)#크기(두께)
    img_regist_ts = models.CharField(null=True, blank=True, max_length=30)#약학정보원 이미지 생성일
    class_no = models.CharField(null=True, blank=True, max_length=30)#분류번호
    class_name = models.CharField(null=True, blank=True, max_length=30)#분류명
    etc_otc_name = models.CharField(null=True, blank=True, max_length=30)#전문/일반
    item_permit_date = models.CharField(null=True, blank=True, max_length=30)#품목허가일자
    form_code_name = models.CharField(null=True, blank=True, max_length=30)#체형코드이름
    mark_code_front_anal = models.CharField(null=True, blank=True, max_length=30)#마크내용(앞)
    mark_code_back_anal = models.CharField(null=True, blank=True, max_length=30)#마크내용(뒤)
    mark_code_front_img = models.CharField(null=True, blank=True, max_length=30)#마크이미지(앞)
    mark_code_back_img = models.CharField(null=True, blank=True, max_length=30)#마크이미지(뒤)
    item_eng_name = models.CharField(null=True, blank=True, max_length=30)#제품 영문명
    change_date = models.CharField(null=True, blank=True, max_length=30)#변경일자
    mark_code_front = models.CharField(null=True, blank=True, max_length=30)#마크코드(앞)
    mark_code_back = models.CharField(null=True, blank=True, max_length=30)#마크코드(뒤)
    edi_code = models.CharField(null=True, blank=True, max_length=30)#보험코드

class OpenPregnatBan(models.Model):
    class meta:
        db_table = 'open_api_임부금기'
    pregnat_medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE, null=True)
    ingr_code = models.CharField(null=True, blank=True, max_length=30) #dur성분코드
    ingr_kor_name = models.CharField(null=True, blank=True, max_length=30) #dur 성분 한국어
    ingr_eng_name = models.CharField(null=True, blank=True, max_length=30) #dur 성분 영어
    item_seq = models.CharField(null=True, blank=True, max_length=30) #품목 기준 코드
    item_name = models.CharField(null=True, blank=True, max_length=30) #품목명
    grade = models.CharField(null=True, blank=True, max_length=2) #등급
    prohbt_content = models.CharField(null=True, blank=True, max_length=200) #금기내용

class OpenOverBan(models.Model):
    class meta:
        db_table = 'open_api_병용금기'
    over_medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE, null=True)
    ingr_code = models.CharField(null=True, blank=True, max_length=30) #dur성분코드
    ingr_kor_name = models.CharField(null=True, blank=True, max_length=30) #dur 성분 한국어
    ingr_eng_name = models.CharField(null=True, blank=True, max_length=30) #dur 성분 영어
    item_seq = models.CharField(null=True, blank=True, max_length=30) #품목 기준 코드
    item_name = models.CharField(null=True, blank=True, max_length=30) #품목명
    mixture_ingr_code = models.CharField(null=True, blank=True, max_length=30) #병용금기 dur성분코드
    mixture_ingr_kor_name = models.CharField(null=True, blank=True, max_length=30) #병용금기 dur 성분 한국어
    mixture_ingr_eng_name = models.CharField(null=True, blank=True, max_length=30) #병용금기 dur 성분 영어
    mixture_item_seq = models.CharField(null=True, blank=True, max_length=30) #병용금기 품목 기준 코드
    mixture_item_name = models.CharField(null=True, blank=True, max_length=30) #병용금기 품목명
    mixture_class_name = models.CharField(null=True, blank=True, max_length=30) #병용금기 약효분류
    prohbt_content = models.CharField(null=True, blank=True, max_length=200) #금기내용

class OpenEfficacyGroupOverlap(models.Model):
    class meta:
        db_table = 'open_api_효능군중복'   
    efficacy_medicine = models.OneToOneField(Medicine, on_delete=models.CASCADE, null=True)
    ingr_code = models.CharField(null=True, blank=True, max_length=30) #dur성분코드
    item_seq = models.CharField(null=True, blank=True, max_length=30) #품목 기준 코드
    item_name = models.CharField(null=True, blank=True, max_length=30) #품목명

class Appraisal(models.Model):
    class meta:
        db_table = '약 코멘트'
    appraisal_medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    compliance_medicine = models.BooleanField(default=False)
    symptom_improvement = models.BooleanField(default=False)
    compliance_medicine_comment = models.CharField(max_length=30, null=True, blank=True)
    symptom_improvement_comment = models.CharField(max_length=30, null=True, blank=True)    

class Pregnat_ban(models.Model):
    class meta:
        db_table = '임부주의'
    pregnat_ingredient_name = models.CharField(max_length=100, null=True, blank=True) #주성분 이름
    pregnat_ingredient_code = models.CharField(max_length=30, null=True, blank=True) #주성분 코드
    pregnat_medicine_code = models.CharField(max_length=30, null=True, blank=True) #약품 코드
    pregnat_medicine_name = models.CharField(max_length=30, null=True, blank=True) #약품 이름
    pregnat_manufacturer_name = models.CharField(max_length=30, null=True, blank=True) #제조사
    pregnat_pbc_no = models.CharField(max_length=30, null=True, blank=True)
    pregnat_pbc_dt = models.CharField(max_length=30, null=True, blank=True)
    pregnat_incmp_grd = models.CharField(max_length=100, null=True, blank=True) #임부금기 등급
    pregnat_note = models.CharField(max_length=100, null=True, blank=True) #설명
    pregnat_version = models.CharField(max_length=30, null=True, blank=True) #버전
    pregnat_pay = models.CharField(max_length=5, null=True, blank=True) #급여인지 비급여인지


class Overlap_ban(models.Model):
    class meta:
        db_table = '병용금기'
    over_medicine_name = models.CharField(max_length=100, null=True, blank=True) #약품 이름
    over_medicine_code = models.CharField(max_length=30, null=True, blank=True) #약품 코드
    over_medicine_object_name = models.CharField(max_length=100, null=True, blank=True) #병용금기인 약품이름
    over_medicine_objcet_code = models.CharField(max_length=30, null=True, blank=True) #병용금기인 약품 코드

class Overlap_caution(models.Model):
    class meta:
        db_table = '병용주의'   
    over_caution_ingredient_name_A = models.CharField(max_length=100, null=True, blank=True)#약 성분 이름
    over_caution_ingredient_code_A = models.CharField(max_length=30, null=True, blank=True)#약 성분 코드
    over_caution_medicine_code_A = models.CharField(max_length=30, null=True, blank=True)#약 코드
    over_caution_medicine_name_A = models.CharField(max_length=100, null=True, blank=True)#약 이름
    over_caution_manufacturer_name_A = models.CharField(max_length=30, null=True, blank=True)#제조사
    over_caution_pay_A = models.CharField(max_length=100, null=True, blank=True)#급여, 비급여
    over_caution_ingredient_name_B = models.CharField(max_length=100, null=True, blank=True)#병용주의약물 약 성분 이름
    over_caution_ingredient_code_B = models.CharField(max_length=30, null=True, blank=True)#병용주의약물 약 성분 코드
    over_caution_medicine_code_B = models.CharField(max_length=30, null=True, blank=True)#병용주의약물 약 코드
    over_caution_medicine_name_B = models.CharField(max_length=100, null=True, blank=True)#병용주의약물 약 이름
    over_caution_manufacturer_name_B = models.CharField(max_length=30, null=True, blank=True)#병용주의약물 제조사
    over_caution_pay_B = models.CharField(max_length=5, null=True, blank=True)#병용주의약물 급여, 비급여
    over_caution_pbc_no = models.CharField(max_length=30, null=True, blank=True)
    over_caution_pbc_dt = models.CharField(max_length=30, null=True, blank=True)
    over_caution_note = models.CharField(max_length=100, null=True, blank=True)#증상설명
    
    