package com.example.myhealthbot;

import android.content.Context;
import android.graphics.Bitmap;
import android.util.Log;

import com.google.gson.JsonObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

import okhttp3.MediaType;
import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.http.Part;

public class RequestHttp {
    private static final String HOST = "http://203.252.231.126/";
    private static RequestHttp requestHttp=null;
    Retrofit retrofit;
    RetrofitApi retrofitApi;

    private RequestHttp() {

        retrofit = new Retrofit.Builder()
                .baseUrl(HOST)
                .addConverterFactory(GsonConverterFactory.create())
                .build();
        retrofitApi = retrofit.create(RetrofitApi.class);
    }
    public static String getUrl(){
        return HOST;
    }
    public static RequestHttp getInstance(){
        if (requestHttp == null) {
            requestHttp = new RequestHttp();
        }
        return requestHttp;
    }


    // 이미지 업로드
    public Call<JsonObject> uploadImage(File f,String user_id ) throws IOException {



        RequestBody reqFile = RequestBody.create(MediaType.parse("image/*"), f);
        MultipartBody.Part body = MultipartBody.Part.createFormData("camera", f.getName(), reqFile);
        MultipartBody.Part body2 = MultipartBody.Part.createFormData("user_id", user_id);


        return retrofitApi.postImage(body,body2);
    }

}
