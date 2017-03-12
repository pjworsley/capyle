import sys, inspect, unittest
import numpy as np
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('test')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

from capyle.ca import Neighbourhood

#define global methods
def hascenter(a):
    if a.ndim == 2:
        return (a.shape[0] % 2 == 1 and a.shape[1] % 2 == 1)
    return a.shape[0] % 2 == 1

#----------------------------------------------------------------------

class TestEmpty(unittest.TestCase):
    def test_empty1D(self):
        empty = np.array([])
        control = np.array([0,1,0])
        n = Neighbourhood(empty, dims = 1)
        self.assertTrue(np.array_equal(n.neighbourhood, control))
        
    def test_empty2d(self):
        empty = np.array([[]])
        control = np.zeros((3,3))
        control[1,1] = 1
        n = Neighbourhood(empty)
        self.assertTrue(np.array_equal(n.neighbourhood, control))

#----------------------------------------------------------------------

class TestNeighbourhood2DShapesMeta(type):
    def __new__(mcs, name, bases, dict):
        
        def gen_test_success(arr, testagainst):
            def test(self):
                n = Neighbourhood(arr, dims=2)
                self.assertIsInstance(n, Neighbourhood)
                if type(testagainst) == tuple:
                    self.assertTrue(n.neighbourhood.shape == testagainst)
                else:
                    self.assertTrue(np.array_equal(n.neighbourhood, testagainst))
            return test

        def gen_test_valerr(arr):
            def test(self):
                self.assertRaises(ValueError, Neighbourhood, arr)
            return test

        #set up variables for test
        shapes = []
        emptycontrol = np.zeros((3,3))
        emptycontrol[1,1] = 1
        for i in range(0,5):
            shapes.append((i,)) # single row (centre row of the 3x3 neightbourhood)
            for j in range(0,6):
                shapes.append((i,j))

        for shape in shapes:
            if len(shape) > 1:
                testname = "test_{d}_{a}{b}".format(d=len(shape),a=shape[0], b=shape[1])
            else:
                testname = "test_{d}_{a}".format(d=len(shape),a=shape[0])
            arr = np.empty((shape))
            arr.fill(1)
            if len(shape) > 1:
                #if supplied shape is 2d array
                if shape[0] == 0 or shape[1] == 0:
                    #0 dimensional set to empty neighbourhood
                    dict[testname] = gen_test_success(arr, emptycontrol)
                else:
                    #dimensions > 0
                    if (shape[0] % 2 == 0 or shape[1] % 2 == 0): 
                        #if even dims and hence no center cell
                        dict[testname] = gen_test_valerr(arr)
                    else:
                        #odd dimensions
                        dict[testname] = gen_test_success(arr, (3,3))
            else:
                #if supplied array is 1d
                if shape == (0,):
                    # if dimensions = 0
                    dict[testname] = gen_test_success(arr, emptycontrol)
                else:
                    if shape[0] % 2 == 0:
                        #if shape is even and has no center
                        dict[testname] = gen_test_valerr(arr)
                    else:
                        #else valid array shape
                        dict[testname] = gen_test_success(arr, (3,3))
        return type.__new__(mcs, name, bases, dict) 

class TestNeighbourhood2DShapes(unittest.TestCase, metaclass=TestNeighbourhood2DShapesMeta):
    pass 
#----------------------------------------------------------------------

class TestDimensions2DMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test_success(arr, testagainst):
            def test(self):
                n = Neighbourhood(arr, dims=2)
                self.assertIsInstance(n, Neighbourhood)
                if type(testagainst) == tuple:
                    self.assertTrue(n.neighbourhood.shape == testagainst)
                else:
                    self.assertTrue(np.array_equal(n.neighbourhood, testagainst))
            return test

        def gen_test_valerr(arr):
            def test(self):
                self.assertRaises(ValueError, Neighbourhood, arr)
            return test

        shapes = range(0,7)
        for s in shapes:
            testname = "testdims_{s}".format(s=s)
            newshape = []
            for i in range(s):
                newshape.append(s)
            a = np.ones(newshape)
            if (a.ndim == 1 or a.ndim == 2) and hascenter(a):
                dict[testname] = gen_test_success(a, (3,3))
            else:
                dict[testname] = gen_test_valerr(a)
        return type.__new__(mcs, name, bases, dict)

class TestDimensions2D(unittest.TestCase, metaclass=TestDimensions2DMeta):
    pass

#----------------------------------------------------------------------

class TestNeighbourhood1DShapesMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_test_success(arr, testagainst):
            def test(self):
                n = Neighbourhood(arr, dims=1)
                self.assertIsInstance(n, Neighbourhood)
                if type(testagainst) == tuple:
                    self.assertTrue(n.neighbourhood.shape == testagainst)
                else:
                    self.assertTrue(np.array_equal(n.neighbourhood, testagainst))
            return test

        def gen_test_valerr(arr):
            def test(self):
                l = lambda: Neighbourhood(nhood=arr, dims=1)
                self.assertRaises(ValueError, l)
            return test

        shapes = range(1,5)
        emptycontrol = np.zeros((3))
        emptycontrol[1] = 1


        for shape in shapes:
            testname = "test_1D_{a}".format(a=shape)
            arr = np.ones((shape))
            if (shape == 0):
                dict[testname] = gen_test_success(a, emptycontrol)

            if(shape % 2 == 0):
                dict[testname] = gen_test_valerr(arr)
            else:
                dict[testname] = gen_test_success(arr, (3,))

        return type.__new__(mcs, name, bases, dict)
    
class TestNeighbourhood1DShapes(unittest.TestCase, metaclass=TestNeighbourhood1DShapesMeta):
    pass

#----------------------------------------------------------------------

class TestDimensions1DMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_test_success(arr, testagainst):
            def test(self):
                n = Neighbourhood(arr, dims=1)
                self.assertIsInstance(n, Neighbourhood)
                if type(testagainst) == tuple:
                    self.assertTrue(n.neighbourhood.shape == testagainst)
                else:
                    self.assertTrue(np.array_equal(n.neighbourhood, testagainst))
            return test

        def gen_test_valerr(arr):
            def test(self):
                l = lambda: Neighbourhood(nhood=arr, dims=1)
                self.assertRaises(ValueError, l)
            return test

        # try creating a neighbourhood with 0 to 6 dimensions, only 1 or 2 dimensions should be accepted
        shapes = range(0,7)
        for s in shapes:
            testname = "test_1d_dimensions_{s}".format(s=s)
            newshape = []
            for i in range(s):
                newshape.append(s)
            a = np.ones(newshape)
            if a.ndim == 1 and hascenter(a):
                dict[testname] = gen_test_success(a, (3,))
            else:
                dict[testname] = gen_test_valerr(a)

        return type.__new__(mcs, name, bases, dict)

class TestDimensions1D(unittest.TestCase, metaclass=TestDimensions1DMeta):
    pass

#----------------------------------------------------------------------

class TestDimsArgMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_test_success(arr, dims):
            def test(self):
                n = Neighbourhood(arr, dims=dims)
                self.assertIsInstance(n, Neighbourhood)
            return test

        def gen_test_valerr(arr, dims):
            def test(self):
                l = lambda: Neighbourhood(nhood=arr, dims=dims)
                self.assertRaises(ValueError, l)
            return test


        validarr = np.array([1,1,1])
        t = range(-5,5)
        for i in t:
            testname = "testnhooddims_{i}".format(i=i)
            if i == 1 or i == 2:
                dict[testname] = gen_test_success(validarr, i)
            else:
                dict[testname] = gen_test_valerr(validarr, i)
        
        return type.__new__(mcs, name, bases, dict)

class TestInvalidDimsArg(unittest.TestCase, metaclass=TestDimsArgMeta):
    pass

#----------------------------------------------------------------------

class TestNeighbourhoodTypes(unittest.TestCase):
    def setUp(self):
        self.ls = [[1,1,1],[1,0,1],[1,1,1]]
        self.ndarray = np.array(self.ls)

    def test_ls(self):
        ls_hood = Neighbourhood(self.ls)
        self.assertIsInstance(ls_hood, Neighbourhood)

    def test_nd(self):
        hood = Neighbourhood(self.ndarray)
        self.assertIsInstance(hood, Neighbourhood)

    def test_types(self):
        ls_hood = Neighbourhood(self.ls)
        nd_hood = Neighbourhood(self.ndarray)
        self.assertEqual(type(ls_hood), type(nd_hood))
        self.assertTrue(np.array_equal(ls_hood.neighbourhood, nd_hood.neighbourhood))
        self.assertEqual(type(ls_hood.neighbourhood), type(nd_hood.neighbourhood))

if __name__ == '__main__':
    unittest.main()
