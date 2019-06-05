file = "taxi.png"

water_pic = imread(file);
water_pic_1 = bitget(water_pic, 1);

%figure
%imshow(water_pic);

figure
I = 255*water_pic_1;
imshow(255*water_pic_1);

figure;

I1 = im2bw(I, 0.85);
imshow(I1)

