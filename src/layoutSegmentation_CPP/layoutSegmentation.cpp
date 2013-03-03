#include <cv.h>
#include <cvaux.h>
#include <highgui.h>
#include <cxcore.h>
#include <assert.h>
#include <stdio.h>

using namespace std;
using namespace cv;
RNG rng(12345);
int main ( int argc, char **argv )
{
    printf("argc:%d, argv[0]:%s\n",argc,argv[0]);
    assert(argc>=2);
    char* filename = argv[1];
    int contourType = CV_RETR_EXTERNAL;
    if(argc==3 && argv[2][0]=='T'){
            contourType = CV_RETR_TREE;
        
    }
    Mat imgRGB = imread(filename);
    Mat imgGrey = imread(filename,0); 
    if(imgGrey.empty()){
        cout << "No valid filename for the image"<<endl;
        return -1;
    }
     
    Mat imgCanny;
    Mat imgDil;
    Mat imgErode;
    //blur( imgGrey, imgGrey, Size(2,2) );
    Canny(imgGrey,imgCanny,60,150,3);
    // clear image hearder 
    
    imgCanny(Range(0,19), Range::all()).setTo(0);
    
    namedWindow("test", CV_WINDOW_AUTOSIZE );
    imshow("test",imgCanny);
    Mat se90 = getStructuringElement( MORPH_RECT,Size(7,1),Point(2,0));
    Mat se0 = getStructuringElement( MORPH_RECT,Size(1,5),Point(0,3));
    dilate(imgCanny,imgDil,se90);
    dilate(imgDil,imgDil,se0);

    namedWindow("canny", CV_WINDOW_AUTOSIZE );
    imshow( "canny", imgCanny );
    namedWindow("dilate", CV_WINDOW_AUTOSIZE );
    imshow( "dilate", imgDil );
    //cvFloodFill
    
    Mat seD = getStructuringElement( MORPH_CROSS,Size(3,3),Point(1,1));
    erode(imgDil,imgErode,seD);
    erode(imgErode,imgErode,seD);
    
    int height = imgErode.rows;
    int width = imgErode.cols;
    /*cout<<"rows:"<<width<<" cols:"<<height << endl;
    imgErode.col(0).setTo(255); 
    imgErode.col(width-1).setTo(255); 
    imgErode.row(height-1).setTo(255);*/
    namedWindow("erode", CV_WINDOW_AUTOSIZE );
    imshow( "erode", imgErode);
    

    vector<vector<Point> > v;
    vector<Vec4i> hierarchy;
    findContours(imgErode, v, hierarchy, contourType, CV_CHAIN_APPROX_SIMPLE);
    vector<vector<Point> > contours_poly(v.size());
    vector<Rect> outputRect;
    for(int i = 0; i < v.size(); i++) {
        //printf("%d,%d\n", v[i][0].x, v[i][0].y);
        //approxPolyDP( Mat(v[i]), contours_poly[i], 3, true );
        Rect rect = boundingRect(Mat(v[i]));
        if(rect.area()>20&&rect.height>3){
            cout<<rect.area()<<endl;
            outputRect.push_back(rect);
            Scalar color = Scalar( rng.uniform(0, 255), rng.uniform(0,255), rng.uniform(0,255) ); 
            // Draws the rect in the original image and show it
            rectangle(imgRGB, rect.tl(), rect.br(), color,2,8, 0);
        }
        
    }
    namedWindow("result", CV_WINDOW_AUTOSIZE );
    imshow( "result", imgRGB);

    cout << "output Rectangle"<< endl;
    for(int i = 0; i < outputRect.size(); i++){
        Rect rect = outputRect[i];
        printf("x:%d y:%d w:%d h:%d\n",rect.x,rect.y,rect.width,rect.height);
    }
    cvWaitKey(0);
    return 0;
}

