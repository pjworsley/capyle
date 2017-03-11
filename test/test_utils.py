import unittest, inspect, sys
import numpy as np
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('test')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

from capyle.ca import Grid1D, Neighbourhood
import capyle.utils as utils

class TestClipNumMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_clip_test(i, lowclip, highclip):
            def test(self):
                res = utils.clip_numeric(i, lowclip, highclip)
                if i < lowclip:
                    self.assertTrue(res == lowclip)
                elif i > highclip:
                    self.assertTrue(res == highclip)
                else:
                    self.assertTrue(res == i)
            return test
      
        tempname = "test_clipnum_"
        for i in range(-5,10):
            #clip int
            testname = tempname + "{i}_1_9".format(i=i)
            dict[testname] = gen_clip_test(i, 1, 9)
            #clip float
            i = i/10
            testname = tempname + "{i}_0_1.4".format(i=i)
            dict[testname] = gen_clip_test(i, 0, 1.4)
            testname = tempname + "{i}_-30_1.4".format(i=i)
            dict[testname] = gen_clip_test(i, -30, 1.4) #clip to an -ve int and float
            testname = tempname + "{i}_0_1".format(i=i)
            dict[testname] = gen_clip_test(i, 0, 1) # clip between and 0

        return type.__new__(mcs, name, bases, dict)

class TestClipNum(unittest.TestCase, metaclass=TestClipNumMeta):
    pass

class TestIntToBinary(unittest.TestCase):
    MIN = np.array([0,0,0,0,0,0,0,0])
    MAX = np.array([1,1,1,1,1,1,1,1])
    def test_normal(self):
        case = 32
        self.assertTrue(np.array_equal(utils.int_to_binary(case), [0,0,1,0,0,0,0,0]))
    
    def test_edges(self):
        low = 0
        high = 255
        self.assertTrue(np.array_equal(utils.int_to_binary(low), self.MIN))
        self.assertTrue(np.array_equal(utils.int_to_binary(high), self.MAX))
    
    def test_outside(self):
        #should exhibit clipping behaviour
        low = -1
        high = 256
        cases = low, high
        self.assertTrue(np.array_equal(utils.int_to_binary(low), self.MIN))
        self.assertTrue(np.array_equal(utils.int_to_binary(high), self.MAX))

    def test_non_int(self):
        #floors decimal to int
        case = 23.4
        self.assertTrue(np.array_equal(utils.int_to_binary(case),utils.int_to_binary(int(case))))

class TestScaleArray(unittest.TestCase):
    def test_scale_up(self):
        a = np.ones((10,10))
        toshape = 14, 20
        b = utils.scale_array(a, toshape[0], toshape[1])
        self.assertTrue(b.shape == toshape)
        self.assertTrue(np.array_equal(a, b[:a.shape[0], :a.shape[1]]))

    def test_scale_same(self):
        a = np.ones((10,10))
        toshape = 10,10
        b = utils.scale_array(a, toshape[0], toshape[1])
        self.assertTrue(b.shape == toshape)
        self.assertTrue(np.array_equal(a, b))

    def test_scale_down(self):
        a = np.ones((10,10))
        toshape = 3,6
        b = utils.scale_array(a, toshape[0], toshape[1])
        self.assertTrue(b.shape == toshape)
        self.assertTrue(np.array_equal(b, a[:b.shape[0], :b.shape[1]]))

if __name__ == '__main__':
    unittest.main()
