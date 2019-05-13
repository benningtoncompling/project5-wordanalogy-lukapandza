import os
import sys
import numpy
import math


vector_file = sys.argv[1]
input_directory = sys.argv[2]
output_directory = sys.argv[3]
eval_file = sys.argv[4]
should_normalize = sys.argv[5]
similarity_type = sys.argv[6]


# import the vector file and return a dictionary
# returns a dictionary, pairing each word to a list of 300 numbers
def read_vectors(vector_file):
    vectors = {}
    with open(vector_file, 'r') as open_file:
        lines = open_file.readlines()
        for line in lines:
            vec = line.split()
            word = vec[0]
            nums = []
            for num in vec[1:]:
                num = float(num)
                nums.append(num)
            value = numpy.array(nums, dtype=float)
            vectors[word] = value
    return vectors


def euclidian_distance(vec1, vec2):
    solution = math.sqrt(numpy.sum((vec2 - vec1)**2))
    return solution


def manhattan_distance(vec1, vec2):
    solution = numpy.sum(abs(vec2-vec1))
    return solution


def cosine_distance(vec1, vec2):
    solution = numpy.dot(vec1, vec2) / (math.sqrt(numpy.dot(vec1, vec1)) * math.sqrt(numpy.dot(vec2, vec2)))
    return solution


# generate 1 output file for each input file in directory
def solve_analogies(vectors, input_directory, output_directory, should_normalize, similarity_type):
    for filename in os.listdir(input_directory):
        if filename.startswith('.'):
            continue
        if not filename.endswith('.txt'):
            continue

        filepath_in = os.path.join(input_directory, filename)
        filepath_out = os.path.join(output_directory, filename)

        with open(filepath_in, 'r') as in_file:
            print('working on', filename)
            with open(filepath_out, 'w+') as out_file:
                with open(eval_file, 'a+') as eval:

                    in_lines = in_file.readlines()
                    in_words = []
                    out_words = []
                    for line in in_lines:
                        local_list = line.split()
                        vectors.setdefault(local_list[0], numpy.zeros(300))
                        vectors.setdefault(local_list[1], numpy.zeros(300))
                        vectors.setdefault(local_list[2], numpy.zeros(300)) # Was getting KeyError: 'kwanza', assumin it's not in the vectors list
                        vecs = (vectors[local_list[0]], vectors[local_list[1]], vectors[local_list[2]])
                        in_words.append(local_list[3])

                        if should_normalize == '0': #don't normalize
                            target_vector = vecs[2] + (vecs[1] - vecs[0])

                            if similarity_type == '0': # use euclidian distance <<
                                min_key = list(vectors.keys())[0]
                                min_distance = euclidian_distance(target_vector, vectors[min_key])
                                for x, y in vectors.items():
                                    if euclidian_distance(target_vector, y) < min_distance:
                                        min_key = x
                                        min_distance = euclidian_distance(target_vector, y)
                                sol_line = str(vecs[0]) + ' ' + str(vecs[1]) + ' ' + str(vecs[2]) + ' ' + min_key
                                out_file.write(sol_line)
                                out_file.write('\n')
                                out_words.append(min_key)

                            if similarity_type == '1': # use manhattan distance <<
                                min_key = list(vectors.keys())[0]
                                min_distance = manhattan_distance(target_vector, vectors[min_key])
                                for x, y in vectors.items():
                                    if manhattan_distance(target_vector, y) < min_distance:
                                        min_key = x
                                        min_distance = manhattan_distance(target_vector, y)
                                sol_line = str(vecs[0]) + ' ' + str(vecs[1]) + ' ' + str(vecs[2]) + ' ' + min_key
                                out_file.write(sol_line)
                                out_file.write('\n')
                                out_words.append(min_key)

                            if similarity_type == '2': # use cosine distance >>
                                max_key = list(vectors.keys())[0]
                                max_distance = cosine_distance(target_vector, vectors[max_key])
                                for x, y in vectors.items():
                                    if cosine_distance(target_vector, y) > max_distance:
                                        max_key = x
                                        max_distance = cosine_distance(target_vector, y)
                                sol_line = str(vecs[0]) + ' ' + str(vecs[1]) + ' ' + str(vecs[2]) + ' ' + max_key
                                out_file.write(sol_line)
                                out_file.write('\n')
                                out_words.append(max_key)

                        if should_normalize == '1': #normalize
                            for vec in vecs:
                                vec = vec/math.sqrt(numpy.sum(vec**2))
                            target_vector = vecs[2] + (vecs[1] - vecs[0])

                            if similarity_type == '0': # use euclidian distance <<
                                min_key = list(vectors.keys())[0]
                                min_distance = euclidian_distance(target_vector, vectors[min_key]/math.sqrt(numpy.sum(vectors[min_key]**2)))
                                for x, y in vectors.items():
                                    if euclidian_distance(target_vector, y/math.sqrt(numpy.sum(y**2))) < min_distance:
                                        min_key = x
                                        min_distance = euclidian_distance(target_vector, y/math.sqrt(numpy.sum(y**2)))
                                sol_line = str(vecs[0]) + ' ' + str(vecs[1]) + ' ' + str(vecs[2]) + ' ' + min_key
                                out_file.write(sol_line)
                                out_file.write('\n')
                                out_words.append(min_key)

                            if similarity_type == '1': # use manhattan distance <<
                                min_key = list(vectors.keys())[0]
                                min_distance = manhattan_distance(target_vector, vectors[min_key]/math.sqrt(numpy.sum(vectors[min_key]**2)))
                                for x, y in vectors.items():
                                    if manhattan_distance(target_vector, y/math.sqrt(numpy.sum(y**2))) < min_distance:
                                        min_key = x
                                        min_distance = manhattan_distance(target_vector, y/math.sqrt(numpy.sum(y**2)))
                                sol_line = str(vecs[0]) + ' ' + str(vecs[1]) + ' ' + str(vecs[2]) + ' ' + min_key
                                out_file.write(sol_line)
                                out_file.write('\n')
                                out_words.append(min_key)

                            if similarity_type == '2': # use cosine distance >>
                                max_key = list(vectors.keys())[0]
                                max_distance = cosine_distance(target_vector, vectors[max_key]/math.sqrt(numpy.sum(vectors[max_key]**2)))
                                for x, y in vectors.items():
                                    if cosine_distance(target_vector, y/math.sqrt(numpy.sum(y**2))) > max_distance:
                                        max_key = x
                                        max_distance = cosine_distance(target_vector, y/math.sqrt(numpy.sum(y**2)))
                                sol_line = str(vecs[0]) + ' ' + str(vecs[1]) + ' ' + str(vecs[2]) + ' ' + max_key
                                out_file.write(sol_line)
                                out_file.write('\n')
                                out_words.append(max_key)

                    eval.write(filepath_in)
                    eval.write('\n')
                    cor = 0
                    pos = len(in_words)
                    i = 0
                    while i < pos:
                        if in_words[i] == out_words[i]:
                            cor = cor + 1
                        i = i + 1
                    line2 = 'ACCURACY TOP1: ' + str((cor/pos*100)) + '% ' + '(' + str(cor) + '/' + str(pos) + ')'
                    eval.write(line2)
                    eval.write('\n')


VECTORS = read_vectors(vector_file)
solve_analogies(VECTORS, input_directory, output_directory, should_normalize, similarity_type)
