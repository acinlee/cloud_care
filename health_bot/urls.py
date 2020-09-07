from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

app_name = 'health_bot'

urlpatterns = [
    path('rest_framework/', include('rest_framework.urls', namespace='rest_framework_category')),
    path('app_login/', views.app_signup),
    path('CloudCareMain/', views.main_page, name="main_page"),
    path('CloudCareMainFK/', views.main_page_fk, name="main_page_fk"),
    path('CloudCareMain/<family_pk>/', views.family_choice_page, name="family_choice_page"), #가족 있는 경우 메인 이동
    path('CloudCareMain/disease_date/<family_pk>/', views.disease_main_page, name="di_main_page"),
    path('CloudCareMain/hos_date/<family_pk>/', views.hos_main_page, name="hos_main_page"),
    path('', views.First, name='first_view'),
    path('home/',views.home,name="home"),
    path('Login_view/', views.Login_view, name='login_view'), 
    path('Signup_view/', views.Signup_view, name="signup_view"),
    path('Sign/', views.SignUp, name="signup"),
    path("Login/", views.Login, name="login"),
    path("Logout/", views.Logout, name="logout"),
    path("Pw_reset_view/", views.Pw_reset_view, name="pw_reset_view"),
    path("Pw_reset/", views.Pw_reset, name="pw_reset"),
    path("Mypage/", views.mypage, name="mypage"),
    path("Edit_move/", views.user_edit_go, name="edit_go"),
    path("Edit_user/", views.user_edit, name="user_edit"),
    path("Photo_edit/", views.user_photo_edit, name="user_photo_edit"),
    path('family_page/', views.family_create_page, name="family_page"),
    path('Create_family/', views.family_create, name="family_create"),
    path('family_member_add_go/', views.family_memeber_add_page, name="family_memeber_add_page"),
    path('Pic_prescription/', views.opencv_prescription, name="take_pic_prescription"), #처방전 촬영
    path('Pic_prescription_confirm/', views.opencv_prescription, name="take_pic_prescription"), #처방전 text 추출 정보 확인
    path('prescription_done/', views.prescription_confirm, name="prescription_done"), #처방전 완료
    path('prescription_cancel/<pre_info>/', views.prescription_cancel, name="prescription_cancel"), #처방전 취소
    path('prescription_info/<pre_info>/', views.prescription_detail_info, name="prescription_info"), #처방전 정보 
    path('medicine_info/<medicine_info>/', views.medicine_detail_info, name="medicine_info"), #의약품 상세정보
    path('family_prescription/<family_id>/', views.family_prescription_check, name="family_prescription_check"),#가족처방전 확인
    path('uploadImage/',views.upload_image),
    path('request_family_page/',views.request_family_page,name="request_family_page"),
    path('checkNoti/',views.check_noti,name='check_noti'),
    path('requestFamily/',views.request_family,name="request_family"),
    #ajax
    path('ajax/userFind', views.userFind, name="userFind"), #유저 id 찾기
    path('userAdd/<noti_id>', views.userAdd, name="userAdd"), 
    path('denialAdd/<noti_id>', views.denialAdd, name="denialAdd"), 
    path('ajax/userDelete', views.userDelete, name="userDelete"), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)