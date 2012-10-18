dirInfo = dir('../res')
for i = 1:length(dirInfo)
   if(length(regexpi(dirInfo(i).name,'.*\.png')))
      layoutSegmentation(strcat('../res/',dirInfo(i).name));
      pause
   end
end