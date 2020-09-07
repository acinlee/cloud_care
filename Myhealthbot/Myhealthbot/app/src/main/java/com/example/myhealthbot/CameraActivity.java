package com.example.myhealthbot;



import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.hardware.Camera;
import android.hardware.camera2.CameraDevice;
import android.os.Bundle;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.gson.JsonObject;

import org.json.JSONException;
import org.json.JSONObject;
import org.opencv.android.OpenCVLoader;
import org.opencv.android.Utils;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CameraActivity extends AppCompatActivity implements SurfaceHolder.Callback{

    private CameraDevice camera;
    private SurfaceView mCameraView;
    private ImageView captureBtn;
    private SurfaceHolder mCameraHolder;
    private FrameLayout cameraBorder;
    private Camera mCamera;

    private ImageView imageView;
    private  FrameLayout frameLayout;

    private Opencv opencv;
    private Bitmap rotateBitmap;
    private LinearLayout imageViewContainer;
    private LinearLayout surfaceViewContainer;
    Camera.PictureCallback mPicture = null;
    String userId;
    static {
    if (!OpenCVLoader.initDebug()) {
        // Handle initialization error
    }
}

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_camera);
        userId = getIntent().getStringExtra("user_id");
        mCameraView = (SurfaceView)findViewById(R.id.surfaceView);
        captureBtn  = findViewById(R.id.capture_btn);
        //cameraBorder= findViewById(R.id.camera_border);

        imageView  = findViewById(R.id.imageView);
        frameLayout = findViewById(R.id.frameLayout);
        imageViewContainer = findViewById(R.id.imageViewContainer);
        surfaceViewContainer = findViewById(R.id.surfaceViewContainer);
        opencv = new Opencv();




//
//        moblieSize = new Point();
//        Display display = getWindowManager().getDefaultDisplay();
//        display.getSize(moblieSize);

        init();

        mPicture = new Camera.PictureCallback(){
            @Override
            public void onPictureTaken(byte[] data, Camera camera) {

                BitmapFactory.Options options = new BitmapFactory.Options();
                options.inSampleSize = 8;
                Bitmap bitmap = BitmapFactory.decodeByteArray(data, 0, data.length);
                Matrix matrix = new Matrix();
                matrix.postRotate(90);
                rotateBitmap = Bitmap.createBitmap(bitmap, 0,0,bitmap.getWidth(), bitmap.getHeight(), matrix, true);
//                cameraBorder.getLocationOnScreen(layoutLoc);
//                Bitmap result  = Bitmap.createBitmap(rotateBitmap,layoutLoc[0],layoutLoc[1],cameraBorder.getWidth(),cameraBorder.getHeight());
//                Log.d("point","x:"+layoutLoc[0]+",y:"+layoutLoc[1]);
//                Log.d("point","width:"+cameraBorder.getWidth()+",height:"+cameraBorder.getHeight());
//
                Mat origin = new Mat(rotateBitmap.getWidth(),rotateBitmap.getHeight(), CvType.CV_8UC4);
                Mat origin2 = new Mat(rotateBitmap.getWidth(),rotateBitmap.getHeight(), CvType.CV_8UC4);
                Utils.bitmapToMat(rotateBitmap,origin);
                opencv.setImage(origin);
                opencv.Edge();
                opencv.findMaxContours();
                List<MatOfPoint> contour = opencv.getContours();
                //ArrayList<Integer> maxIndexList = opencv.getMaxIndexList();


                if(opencv.getBorderIndex() != -1) {
                    List<Point> points = opencv.getApproxPoint();
                    Collections.sort(points, new Comparator<Point>() {
                        @Override
                        public int compare(Point p1, Point p2) {
                            double s1 = p1.x + p1.y;
                            double s2 = p2.x + p2.y;
                            return Double.compare(s1, s2);
                        }
                    });




//                    Rect rect = Imgproc.boundingRect(contour.get(opencv.getBorderIndex()));

//                    Log.d("size",contour.get(opencv.getBorderIndex()).size()+"");
//                    Log.d("size","x:"+rect.x+",y:"+rect.y);
//                    Log.d("size","width:"+rect.width+",height:"+rect.height);



                    double width = opencv.getMaxWidth(points.get(0).x,points.get(1).x,points.get(2).x,points.get(3).x);
                    double height = opencv.getMaxHeight(points.get(0).y,points.get(2).y,points.get(1).y,points.get(3).y);

//                    Log.d("size","----------------------");
//                    for(Point p : opencv.getApproxPoint()){
//                        Log.d("size","x: "+p.x+", y: "+p.y);
//                    }
//                    Log.d("size","----------------------");
//                    for(Point p : points){
//                        Log.d("size","x: "+p.x+", y: "+p.y);
//                    }
//                    Log.d("size","----------------------");
                    MatOfPoint2f src = new MatOfPoint2f(
                            points.get(0),
                            points.get(1),
                            points.get(2),
                            points.get(3));
                    MatOfPoint2f dst = new MatOfPoint2f(
                            new org.opencv.core.Point(0,0),
                            new org.opencv.core.Point(width-1,0),
                            new org.opencv.core.Point(0,height-1),
                            new org.opencv.core.Point(width-1,height-1)
                    );

                    Mat warpMat = Imgproc.getPerspectiveTransform(src,dst);

                   Imgproc.warpPerspective(origin, origin, warpMat, new Size(width,height));
                   Imgproc.resize(origin,origin,new Size(730,950));

//
                    Log.d("size",origin.rows()+"X"+origin.cols());
                    Imgproc.rectangle(origin, new Point(211,188), new Point(400,223 ),new Scalar(76,255,0),-1);



                    //rotateBitmap = Bitmap.createBitmap(rotateBitmap,rect.x,rect.y,rect.width,rect.height);

                    //Imgproc.drawContours(origin, contour, opencv.getBorderIndex(), new Scalar(0, 255, 0), 3);



                    Imgproc.cvtColor(origin,origin,Imgproc.COLOR_RGBA2GRAY);
                    Imgproc.adaptiveThreshold(origin,origin, 255, Imgproc.ADAPTIVE_THRESH_MEAN_C, Imgproc.THRESH_BINARY, 21, 10);

                    rotateBitmap = Bitmap.createBitmap(origin.cols(), origin.rows(), Bitmap.Config.ARGB_8888);
                    Utils.matToBitmap(origin, rotateBitmap);




                    surfaceViewContainer.setVisibility(View.GONE);
                    imageViewContainer.setVisibility(View.VISIBLE);
                    imageView.setImageBitmap(rotateBitmap);

                }else{
                    Toast.makeText(getApplicationContext(), "처방전을 인식할수 없습니다 재촬영해주세요.",Toast.LENGTH_LONG).show();

                }


                mCamera.startPreview();



            }
        };
        captureBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
              //  new Async().execute();
                mCamera.takePicture(null,null,mPicture);


            }
        });



    }

    public void uploadImage(View v){
        File f = new File(getApplicationContext().getCacheDir(), "temp.jpeg");
        OutputStream out = null;
        try {
            f.createNewFile();
            out = new FileOutputStream(f);
            rotateBitmap.compress(Bitmap.CompressFormat.JPEG, 100, out);

            Call<JsonObject> call =RequestHttp.getInstance().uploadImage(f,userId);
            call.enqueue(new Callback<com.google.gson.JsonObject>() {
                @Override
                public void onResponse(Call<JsonObject> call, Response<JsonObject> response) {
                    Log.d("is","성공");
                    Intent intent = new Intent();
//                    intent.putExtra("result", "some value");
                    setResult(RESULT_OK, intent);
                    finish();


                }

                @Override
                public void onFailure(Call<JsonObject> call, Throwable t) {
                    Log.d("is","실패");
                }

            });
        } catch (IOException e) {
            e.printStackTrace();
        }finally {
            try { out.close(); } catch (IOException e) { e.printStackTrace(); }

        }

    }


    private void init(){


        mCameraHolder = mCameraView.getHolder();
        mCameraHolder.addCallback(this);
    }
    private Camera.Size getOptimalPreviewSize(List<Camera.Size> sizes, int width, int height) {
        final double ASPECT_TOLERANCE = 0.05;
        double targetRatio = (double) width / height;
        if (sizes == null) {
            return null;
        }

        Camera.Size optimalSize = null;
        double minDiff = Double.MAX_VALUE;

        int targetHeight = height;


        for (Camera.Size size : sizes) {
            double ratio = (double) size.width / size.height;
            if (Math.abs(ratio - targetRatio) > ASPECT_TOLERANCE) {
                continue;
            }
            if (Math.abs(size.height - targetHeight) < minDiff) {
                optimalSize = size;
                minDiff = Math.abs(size.height - targetHeight);
            }
        }


        if (optimalSize == null) {
            minDiff = Double.MAX_VALUE;
            for (Camera.Size size : sizes) {
                if (Math.abs(size.height - targetHeight) < minDiff) {
                    optimalSize = size;
                    minDiff = Math.abs(size.height - targetHeight);
                }
            }
        }
        Log.i("optimal size", ""+optimalSize.width+" x "+optimalSize.height);
        return optimalSize;
    }


    @Override
    public void surfaceCreated(SurfaceHolder holder) {
        mCamera = Camera.open();
        mCamera.setDisplayOrientation(90);
        Camera.Parameters parameters = mCamera.getParameters();
        parameters.setFocusMode(Camera.Parameters.FOCUS_MODE_CONTINUOUS_VIDEO);

        List<Camera.Size> sizes = parameters.getSupportedPictureSizes();
        Camera.Size optimalSize;
        optimalSize = getOptimalPreviewSize(sizes, parameters.getPreviewSize().width, parameters.getPreviewSize().height);
        parameters.setPictureSize(optimalSize.width, optimalSize.height);
        mCamera.setParameters(parameters);

        try {
            mCamera.setPreviewDisplay(mCameraHolder);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

@Override
    public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {

        mCamera.startPreview();
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder) {
        mCamera.stopPreview();
        mCamera.release();
        mCamera = null;
    }


}

