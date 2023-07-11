function h = plotNAVsignals(data,mode)
%plotNAVsignals plots the Naval dataset (2Dim). X vs Y plot.

if nargin < 2
   mode = "mc";
end

[traces, t, labels] = v2struct(data);

[nobj, ndim, ntime] = size(traces);

nlabels = max(labels);   

if mode == "1c"
    clabels = zeros(nobj,1);
    clabels = char(clabels);
    clabels(1:nobj) = 'b';  
elseif mode == "2c"     
    clabels = zeros(nobj,1);
    clabels = char(clabels);
    idx_1 = (labels ==  1);
    clabels( idx_1) = 'g';
    clabels(~idx_1) = 'r';
else % mode == "mc" 
    cols = defColorLines(nlabels);
    clabels = zeros(nobj,3);
    for i = 1:nobj
        clabels(i,:) = cols(labels(i),:);
    end
end

h = figure();
hold on
for i = 1:size(traces,1)
    x = reshape(traces(i,1,:),ntime,1);
    y = reshape(traces(i,2,:),ntime,1);
    plot(x, y, 'Color', clabels(i,:));
end

%axis([0 80 15 45])
%axis([0 1 0 1])
xlabel ('x (dam)') 
ylabel ('y (dam)')
title('Naval scenario')

end
