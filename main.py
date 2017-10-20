import os
import numpy
from dp import DynamicProgrammer
from PIL import Image
template_folder = ".\\extracted_mfcc\\a"
test_folder = '.\\extracted_mfcc\\b'
all_template_matrix = {}
all_test_matrix = {}
numpy.set_printoptions(precision=2)
numpy.set_printoptions(threshold=numpy.nan)
numpy.set_printoptions(linewidth=9999)
for file_name in os.listdir(template_folder):
    file_prefix = file_name[0:3]
    all_template_matrix[file_prefix] = numpy.loadtxt(template_folder+"\\"+file_name, dtype=numpy.float)
for file_name in os.listdir(test_folder):
    file_prefix = file_name[0:3]
    all_test_matrix[file_prefix] = numpy.loadtxt(test_folder + "\\" + file_name, dtype=numpy.float)
score = []
for temp_key, template_matrix in all_template_matrix.items():
    best_score = float('inf')
    for test_key, test_matrix in all_test_matrix.items():
        dp = DynamicProgrammer(template_matrix, test_matrix)
        min_path_score, min_path, path_matrix = dp.get_min_path()
        score.append(min_path_score)
        print(temp_key + ' vs ' + test_key + ': ' + str(min_path_score))
        if min_path_score < best_score:
            best_score = min_path_score
            best_match = test_key
            best_matrix = path_matrix
        numpy.savetxt('.\\var\\dump\\' + temp_key + '_' + test_key + '_distort.txt', numpy.flipud(dp.get_distortion()), fmt='%d')
        numpy.savetxt('.\\var\\dump\\' + temp_key + '_' + test_key + '_acc.txt', numpy.flipud(dp.get_accumulated()), fmt='%d')
        numpy.savetxt('.\\var\\path\\all\\' + temp_key + '_' + test_key + '_path.txt', numpy.flipud(path_matrix), fmt='%d')
        img = Image.fromarray(numpy.asarray(numpy.flipud(path_matrix.astype('uint8') * 255)))
        img.save('.\\var\\path_pic\\all\\' + temp_key + '_' + test_key + '.jpg')
    numpy.savetxt('.\\var\\path\\best_match\\' + temp_key + '_' + best_match + '_path.txt', numpy.flipud(best_matrix), fmt='%d')
    print('Best match for ' + temp_key + ': ' + best_match)
    img = Image.fromarray(numpy.flipud(numpy.asarray(best_matrix.astype('uint8') * 255)))
    img.save('.\\var\\path_pic\\best_match\\' + temp_key + '_' + best_match + '.jpg')
score_matrix = numpy.matrix(score)
score_matrix = numpy.flipud(score_matrix.reshape((len(all_template_matrix), len(all_template_matrix))))
numpy.savetxt('score_matrix.txt', score_matrix, fmt='%10d')
