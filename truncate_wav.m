clear;
folder = '.\wav\original\';
dest = '.\wav\truncated\';
duration = 0.72;
files = dir(folder);
threshold = 0.01;
for i = 3:length(files)
  [data, frameRate] = audioread(strcat('.\wav\original\', files(i).name));
  energyMatrix = data.^2;
  n = 1;
  startIndex = 0;
  while (n <= length(energyMatrix) && startIndex == 0)
      if (abs(energyMatrix(n)) > threshold && 
        abs(energyMatrix(n+1)) > threshold && 
        abs(energyMatrix(n+2)) > threshold );
          startIndex = n;
      end
      n = n + 1;
  end
  if (startIndex + duration * frameRate > length(data))
    startIndex = length(data) - duration * frameRate;
  end
  data = data(startIndex:startIndex+round(duration*frameRate));
  audiowrite(strcat(dest, files(i).name), data, frameRate);
end
  
