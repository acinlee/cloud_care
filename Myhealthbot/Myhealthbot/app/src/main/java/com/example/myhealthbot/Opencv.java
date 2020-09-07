package com.example.myhealthbot;

import android.util.Log;

import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.MatOfPoint;
import org.opencv.core.MatOfPoint2f;
import org.opencv.core.Point;
import org.opencv.core.Scalar;
import org.opencv.core.Size;
import org.opencv.imgproc.Imgproc;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class Opencv {
    Mat matInput;
    Mat matResult;
    Mat originSrc;
    private int consMaxIndex = -1;
    private List<MatOfPoint> contours;
    private  int borderIndex = -1;
    private int max=0;
    private MatOfPoint2f approx;


   public Opencv(){
       approx = new MatOfPoint2f();

   }

    public void setImage(Mat originSrc){
        this.originSrc = originSrc;
        matInput = new Mat(originSrc.rows(), originSrc.cols(), originSrc.type());

        Imgproc.cvtColor(originSrc,matInput, Imgproc.COLOR_RGB2GRAY);
        if ( matResult == null )
            matResult = new Mat(matInput.rows(), matInput.cols(), matInput.type());

    }
    public Mat getImage(){
       return matResult;
    }

    public void Edge(){
//        Mat blur = new Mat(matInput.rows(), matInput.cols(), matInput.type());
//        final Size ksize = new Size(5, 5);
//        Imgproc.GaussianBlur(matInput, blur, ksize, 0);
        //50 150
        Imgproc.Canny(matInput,matResult,50,150);
        Mat kernel = new Mat(new Size(3, 3), CvType.CV_8UC1, new Scalar(255));
        Imgproc.morphologyEx(matResult, matResult, Imgproc.MORPH_CLOSE, kernel);

    }

    public void findMaxContours(){
        contours = new ArrayList<>();
        Imgproc.findContours(matResult,contours,new Mat(),Imgproc.RETR_TREE,Imgproc.CHAIN_APPROX_SIMPLE);
        double maxArea = 0;
        int max_idx = -1;

        Collections.sort(contours, new Comparator<MatOfPoint>() {
            @Override

            public int compare(MatOfPoint m1, MatOfPoint m2) {
                if (Imgproc.contourArea(m1) < Imgproc.contourArea(m2)) {
                    return -1;
                } else if (Imgproc.contourArea(m1) > Imgproc.contourArea(m2)) {
                    return 1;
                }
                return 0;
            }
        });



        for(int i=contours.size()-10; i<contours.size(); i++){
            double area = Imgproc.contourArea(contours.get(i));

            double epsilon = 0.02*Imgproc.arcLength(new MatOfPoint2f(contours.get(i).toArray()),true);

            Imgproc.approxPolyDP(new MatOfPoint2f(contours.get(i).toArray()),approx,epsilon,true);

            if (approx.size().height == 4 &&
                    area/(originSrc.rows()*originSrc.cols())>0.1) {

                borderIndex = i;
                break;
            }


        }


//
//        for(int i=contours.size()-6; i<contours.size(); i++){
//            double area = Imgproc.contourArea(contours.get(i));
//
//            double epsilon = 0.02*Imgproc.arcLength(new MatOfPoint2f(contours.get(i).toArray()),true);
//            MatOfPoint2f approx = new MatOfPoint2f();
//            Imgproc.approxPolyDP(new MatOfPoint2f(contours.get(i).toArray()),approx,epsilon,true);
//
//            if (area > maxArea  &&
//                    approx.size().height == 4 &&
//                    area/(originSrc.rows()*originSrc.cols())>0.1) {
//                Log.d("point",i+"");
//                maxArea = area;
//                borderIndex = (max_idx == -1) ? i : max_idx;
//                max_idx = i;
//
//
//            }
//
//
//        }


    }
    public int getBorderIndex(){return borderIndex;}
    public List<MatOfPoint> getContours(){
        return contours;
    }
    public int getMax(){return max;}

//    public ArrayList<Integer> getMaxIndexList(){return getMaxIndexList();}


    public List<Point> getApproxPoint(){return approx.toList();}
    public double getMaxHeight(double y1, double y2, double y3, double y4){
        double h1 = Math.abs(y2-y1);
        double h2 = Math.abs(y4-y3);
        return (h1 > h2) ? h1 : h2;
    }
    public double getMaxWidth(double x1, double x2, double x3, double x4){
        double w1 = Math.abs(x2-x1);
        double w2 = Math.abs(x4-x3);

        return (w1 > w2) ? w1:w2;
    }
}
