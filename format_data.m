function [ output_args ] = format_data( filename)
%FORMAT_DATA Summary of this function goes here
%   Detailed explanation goes here
fprintf('-- STARTING: combenefit file parsing program --\n');
fprintf('generating test folder for: %s\n', filename);
[root, fname, extn] = fileparts(filename);
dirname = strcat('combenefit_', fname);
fprintf('making folder: "%s"\n', dirname);
if exist(dirname) == 7  
    fprintf('-- EXITING: Error -- \n', dirname);
    fprintf('folder "%s" already exists! no doing anything\n', dirname);
    fprintf('remove "%s" is you wish to regenerate\n', dirname);
    return;
end
% make folder
mkdir(dirname);
% read file
[num, raw, txt] = xlsread(filename);







end

