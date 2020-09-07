package com.example.myhealthbot;


import com.google.gson.JsonObject;

import okhttp3.MultipartBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface RetrofitApi {
        @Multipart
        @POST("uploadImage/")
        Call<JsonObject> postImage(@Part MultipartBody.Part image,@Part MultipartBody.Part user);
    }


