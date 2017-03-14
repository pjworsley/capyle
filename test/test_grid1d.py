import unittest, inspect, sys
import numpy as np
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('test')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

from capyle.ca import Grid1D, Neighbourhood, CAConfig

#----------------------------------------------------------------------

class TestNumGensMeta(type):
    def __new__(mcs, name, bases, dict):
        
        def gen_test_success(gens, config, transfunc):
            def test(self):
                config.num_generations = gens
                g = Grid1D(config, transfunc)
                self.assertIsInstance(g, Grid1D)
            return test

        def gen_test_valerr(gens, config, transfunc):
            def test(self):
                config.num_generations = gens
                self.assertRaises(ValueError, lambda c=config: Grid1D(config, transfunc))
            return test
                
        config = CAConfig("test/testdescriptions/1dbasic.py")
        config.states = 0,1
        testgens = range(-1, 6)

        def transfunc(self, grid, neighbourcounts):
            return grid
    
        for g in testgens:
            testname = "test_1d_numgens_{i}".format(i=g)
            config.num_generations = g
            if g < 1:
                dict[testname] = gen_test_valerr(g, config, transfunc)
            else:
                dict[testname] = gen_test_success(g, config, transfunc)
        return type.__new__(mcs, name, bases, dict)

class TestNumGens(unittest.TestCase, metaclass=TestNumGensMeta):
    pass

#----------------------------------------------------------------------

class TestWrap(unittest.TestCase):
    def setUp(self):
        self.config = CAConfig("test/testdescriptions/1dbasic.py")
        self.config.num_generations = 100
        self.config.states = 0,1
        self.config.dimensions = 1
        self.config.nhood_arr = [1,1,1]

    def transfunc(self, grid, neighbourcounts):
        return grid[0]

    def extractsides(self, g):
        e = g[:, -1] 
        w = g[:, 0]
        return e,w

    def iswrapcorrect(self, g, wrap):
        we, ww = self.extractsides(g.wrapping_grid)
        if wrap:
            e = np.array_equal(g.grid[:, -1] , ww)
            w = np.array_equal(g.grid[:, 0] , we)
            sides = e and w
            return sides 
        
        return np.count_nonzero(we) == 0 and np.count_nonzero(ww) == 0

    def case(self, numgens, wrap):
        self.config.wrap = wrap
        g = Grid1D(self.config, self.transfunc)
        randgrid = np.random.randint(0,2, g.grid.shape)
        g.grid[:,:] = randgrid[:,:]
        g.refresh_wrap()
        self.assertTrue(self.iswrapcorrect(g, wrap))
         #set outer values to 4 which cannot already be in the grid and verify match again
        g.grid[0, :] = 4
        g.grid[-1, :] = 4
        g.refresh_wrap()
        self.assertTrue(self.iswrapcorrect(g, wrap))

    def test_wrap_1(self):
        #Test smallest avaliable grid size
        gens = 1
        self.case(gens, True)
    
    def test_wrap_2(self):
        #Test smallest avaliable grid size
        gens = 1
        self.case(gens, False)
        #test larger grid
    def test_wrap_3(self):
        gens = 200
        self.case(gens, True)
    def test_wrap_4(self):
        gens = 200
        self.case(gens, False)

#----------------------------------------------------------------------
class TestInitialGridSetMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test_array_eq(a, b):
            def test(self):
                self.assertTrue(np.array_equal(a,b))
            return test

        config = CAConfig("test/testdescriptions/1dbasic.py")
        config.num_generations = 20
        config.states = 0,1
        config.dimensions = 1
        config.nhood_arr = [1,1,1]

        def transfunc(self, grid, neighbourcounts):
            return grid[0]

        numgens = 20
        sizes = range(numgens*2, numgens*2+3)
        for s in sizes:
            testname = "test_initial_grid_set_{s}".format(s=s)
            initialgrid = np.array([np.random.randint(0, 2, s)])
            config.initial_grid = initialgrid
            g = Grid1D(config, transfunc)
            #check that the first lines match
            if s < g.grid.shape[1]:
                dict[testname] = gen_test_array_eq(g.grid[0, :s], initialgrid[0])
            else:
                dict[testname] = gen_test_array_eq(g.grid[0], initialgrid[0, :g.grid.shape[1]])
        return type.__new__(mcs, name, bases, dict)

class TestInitialGridSet(unittest.TestCase, metaclass=TestInitialGridSetMeta):
    pass

#----------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
