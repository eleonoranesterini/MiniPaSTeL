% This script plots the Naval dataset

load Naval_2C
load Naval_3C
% load Naval_3C_S01
% load Naval_3C_SZ

data = extractRandomSubset(data,0.1);
% 
% plotSignals(data);
plotNAVsignals(data);

data2= importdata('Naval_2C');
data3 = importdata('Naval_3C');

