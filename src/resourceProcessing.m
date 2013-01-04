dirInfo = dir('../res')
if (exist('../data') ~= 7)
   mkdir('../data')
end
for i = 1:length(dirInfo)
   if(length(regexpi(dirInfo(i).name,'.*\.png')))
       filename = strrep(dirInfo(i).name,'png','dat');
       filename =strcat('../data/',filename);
       fid = fopen(filename, 'w');
       boxList = layoutSegmentation(strcat('../res/',dirInfo(i).name));
       %% write to file
       d = size(boxList);
       for i = 1:d(2)
         box = boxList(:,i);
	 fprintf(fid,'%d %d %d %d\n',round(box(1)), round(box(2)), round(box(3)), round(box(4)));
         
       end
      fclose(fid);
   end

end
