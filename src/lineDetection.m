function lines = lineDetection(path)
RGB = imread(path);
I = rgb2gray(RGB);
figure,imshow(RGB)
[BW, threshold] = edge(I,'canny','vertical');
% display the original image

% display the hough matrix
[H,T,R] = hough(BW);
[r,c,hnew] = houghpeaks(H,10, ceil(0.3*max(H(:))));
lines = houghlines(BW,T,R,r,c,10,5);
max_len = 0;
figure,imshow(BW),title('original image');
hold on;
for k = 1:length(lines)
   xy = [lines(k).point1; lines(k).point2];
   plot(xy(:,2),xy(:,1),'LineWidth',2,'Color','green');
   % Plot beginnings and ends of lines
   plot(xy(1,2),xy(1,1),'x','LineWidth',2,'Color','yellow');
   plot(xy(2,2),xy(2,1),'x','LineWidth',2,'Color','red');
   % Determine the endpoints of the longest line segment
   len = norm(lines(k).point1 - lines(k).point2);
   if ( len > max_len)
      max_len = len;
      xy_long = xy;
   end
end
% highlight the longest line segment
plot(xy_long(:,2),xy_long(:,1),'LineWidth',2,'Color','cyan');
hold off;

