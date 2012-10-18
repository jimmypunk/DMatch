function boxList = layoutSegmentation(path, property)
RGB = imread(path);
I = rgb2gray(RGB);
%figure, imshow(I), title('original image');
text(size(I,2),size(I,1)+15, ...
    'Image courtesy of Alan Partin', ...
    'FontSize',7,'HorizontalAlignment','right');
text(size(I,2),size(I,1)+25, ....
    'Johns Hopkins University', ...
    'FontSize',7,'HorizontalAlignment','right');
%[haha, threshold] = edge(I, 'sobel');
%fudgeFactor = .5;
%BWs = edge(I,'sobel', threshold * fudgeFactor);
[BWs ,threshold] = edge(I,'canny');
%figure, imshow(BWs), title('binary gradient mask');
se90 = strel('line', 3, 90);
se0 = strel('line', 3, 0);
BWsdil = imdilate(BWs, [se90 se0]);
%figure, imshow(BWsdil), title('dilated gradient mask');
BWdfill = imfill(BWsdil, 'holes');
%figure, imshow(BWdfill),title('binary image with filled holes');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

BWnobord = imclearborder(BWdfill, 4);
%figure, imshow(BWnobord), title('cleared border image');
BWnobord = imclearborder(BWdfill, 4);
%figure, imshow(BWnobord), title('cleared border image');
seD = strel('diamond',1);
BWfinal = imerode(BWnobord,seD);
BWfinal = imerode(BWfinal,seD);
%figure, imshow(BWfinal), title('segmented image');
%figure, imshow(RGB), title('original image');
figure, imshow(RGB), title('original image');
hold on;

%% draw boundingBox
L = bwlabel(BWfinal);
s = regionprops(L,'All');
areaList = zeros(1,length(s));
boxList = zeros(4, length(s));
for i = 1:length(s)
   areaList(i) = s(i).Area;
   boxList(:,i) = s(i).BoundingBox;
end
meanArea = mean(areaList);
for i = 1:length(s)
   %if(areaList(i)>meanArea)
      %subImage = imcrop(I, s(i).BoundingBox);
      %%figure, imshow(subImage);
      rectangle('Position',s(i).BoundingBox,'EdgeColor','g');
   %end
end
hold off;
%hist(areaList);
%BWoutline = bwperim(BWfinal);
%Segout = I;
%Segout(BWoutline) = 255;
%figure, imshow(Segout), title('outlined original image');

