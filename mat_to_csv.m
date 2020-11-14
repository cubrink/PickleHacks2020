FileData = load('wiki.mat');

filepath_matrix = transpose(FileData.wiki.full_path);
name_matrix = transpose(FileData.wiki.name);
gender_matrix = transpose(FileData.wiki.gender);

filepath_matrix{1}
name_matrix{1}
gender_matrix(1)

gender_matrix_cell = num2cell(gender_matrix);

final_matrix = [filepath_matrix, name_matrix, gender_matrix_cell];
final_matrix_2 = [];


[rows, cols] = size(final_matrix);
fid = fopen('wiki_data_updated_delim.csv', 'w');
for i = 1:rows
  fprintf(fid, "%s| %s| %f\n", final_matrix{i,:});
end
fclose(fid);
