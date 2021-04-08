'''
Created on Aug 8, 2016
Processing datasets. 

@author: Xiangnan He (xiangnanhe@gmail.com)
'''
import scipy.sparse as sp
import numpy as np
import os


class Dataset(object):
    '''
    classdocs
    '''

    def __init__(self, path):
        '''
        Constructor
        '''
        self.trainMatrix = self.load_rating_file_as_matrix(path + ".train.rating")
        self.testRatings = self.load_rating_file_as_list(path + ".test.rating")
        self.testNegatives = self.load_negative_file(path + ".test.negative")
        assert len(self.testRatings) == len(self.testNegatives)

        self.num_users, self.num_items = self.trainMatrix.shape

    def load_rating_file_as_list(self, filename):
        ratingList = []
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                user, item = int(arr[0]), int(arr[1])
                ratingList.append([user, item])
                line = f.readline()
        return ratingList

    def load_negative_file(self, filename):
        negativelist = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                line = f.readline()
                while line != None and line != "":
                    arr = line.split("\t")
                    negatives = []
                    for x in arr[1:]:
                        negatives.append(int(x))
                    negativelist.append(negatives)
                    line = f.readline()
                return negativelist
        else:
            with open(filename, "w") as fw:
                nums_test = len(self.testRatings)
                max_id = 0
                for index in xrange(nums_test):
                    pair = self.testRatings[index]
                    max_id = max(pair[1], max_id)

                print "find maxId : " + str(max_id)
                for i in xrange(nums_test):
                    print "processing: " + str(i) + "/" + str(nums_test)
                    pair = tuple(self.testRatings[i])
                    lines = ''
                    lines += str(pair)
                    for t in xrange(99):
                        j = np.random.randint(max_id)
                        while (pair[0], j) in self.testRatings:
                            j = np.random.randint(nums_test)
                        lines += '\t'
                        lines += str(j)
                        negativelist.append(j)
                    print lines
                    fw.writelines(lines)
                    fw.writelines('\n')
                fw.flush()
                fw.close()
                print "!!!write negative list finished!!!"
                return negativelist

    def load_rating_file_as_matrix(self, filename):
        '''
        Read .rating file and Return dok matrix.
        The first line of .rating file is: num_users\t num_items
        '''
        # Get number of users and items
        num_users, num_items = 0, 0
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                u, i = int(arr[0]), int(arr[1])
                num_users = max(num_users, u)
                num_items = max(num_items, i)
                line = f.readline()
        # Construct matrix
        mat = sp.dok_matrix((num_users + 1, num_items + 1), dtype=np.float32)
        with open(filename, "r") as f:
            line = f.readline()
            while line != None and line != "":
                arr = line.split("\t")
                user, item, rating = int(arr[0]), int(arr[1]), float(arr[2])
                if (rating > 0):
                    mat[user, item] = 1.0
                line = f.readline()
        return mat
