function [ title, drugs, units, concentrations, tables] = read_data( filename )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
[num, txt, raw] = xlsread(filename);
% parse title
title = raw(1,1);
% parse concentration axes
concentration_axes = raw(3:4, :);
[rows, cols] = size(concentration_axes);
for col = 1:cols
    if isnan(concentration_axes{1,col})
        break;
    end
end

table_row_count = col-1;
concentration_axes = concentration_axes(1:2,1:table_row_count);

drugs = concentration_axes(1:2, 1);
units = concentration_axes(1:2, 2);

concentrations = cell2mat(concentration_axes(1:2,3:end))';
% parse tables
[raw_row_count, cols] = size(raw);
table_start = 6;
tables = [];
while 1
    fprintf('%d',table_start);
    if and(table_start <= raw_row_count, not(isnan(raw{table_start, 1})))
        fprintf('read table\n');
        table_start = table_start + table_row_count;
    else
        fprintf('done\n');
        break;
    end
end


    








end

