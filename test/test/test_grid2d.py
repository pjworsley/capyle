import sys, inspect, unittest
import numpy as np
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('test')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

from capyle.ca import Grid2D, Neighbourhood, CAConfig

#----------------------------------------------------------------------

class TestGridShapesMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_test_success(d, config, transfunc, expectedshape):
            def test(self):
                config.grid_dims = d
                g = Grid2D(config, transfunc)
                self.assertIsInstance(g, Grid2D)
                self.assertEqual(g.grid.shape, expectedshape)
            return test

        def gen_test_valerr(d, config, transfunc):
            def test(self):
                config.grid_dims = d
                l = lambda c=config: Grid2D(c, transfunc)
                self.assertRaises(ValueError, l)
            return test

        config = CAConfig('test/testdescriptions/2dbasic.py')
        dimensions = 2
        config.states = 0,1,2
        config.nhood_arr = [1,1,1]
        shapes = range(0, 5)

        def transfunc(grid, neighbourcounts):
            return grid
    
        for i in shapes:
            for j in shapes:
                testname = "test_grid_2d_{i}{j}".format(i=i, j=j)
                testdims = (i, j)
                if i < 3 or j < 3:
                    dict[testname] = gen_test_valerr(testdims, config, transfunc)
                else:
                    dict[testname] = gen_test_success(testdims, config, transfunc, (i,j))

        return type.__new__(mcs, name, bases, dict)

class TestGridShapes(unittest.TestCase, metaclass=TestGridShapesMeta):
    pass

#----------------------------------------------------------------------
                    
class TestWrap(unittest.TestCase):
    def setUp(self):
        self.config = CAConfig('test/testdescriptions/2dbasic.py')
        self.dimensions = 2
        self.config.states = 0,1,2
        self.config.nhood_arr = [1,1,1]

    def transfunc(self, grid, neighbourcounts):
        return grid

    def extractsides(self, g):
        n = g[0, 1:-1]
        e = g[1:-1, -1] 
        s = g[-1, 1:-1]
        w = g[1:-1, 0]
        return n, e, s, w

    def iswrapcorrect(self, g):
        wn, we, ws, ww = self.extractsides(g.wrapping_grid)
        n = np.array_equal(g.grid[0] , ws)
        e = np.array_equal(g.grid[:, -1] , ww)
        s = np.array_equal(g.grid[-1] , wn)
        w = np.array_equal(g.grid[:, 0] , we)
        sides = n and e and s and w

        nw = g.grid[0,0] == g.wrapping_grid[-1,-1]
        ne = g.grid[0, -1] == g.wrapping_grid[-1, 0]
        se = g.grid[-1,-1] == g.wrapping_grid[0,0]
        sw = g.grid[-1, 0] == g.wrapping_grid[0,-1]
        corners = nw and ne and sw and se

        return sides and corners

    def case(self, gridshape):
        #fill with random values from 0 - 2
        self.config.grid_dims = gridshape
        self.config.initial_grid = np.random.randint(0,3, gridshape)

        g = Grid2D(self.config, self.transfunc)
        self.assertTrue(self.iswrapcorrect(g))
        #set outer values to 4 which cannot already be in the grid and verify match again
        g.grid[0, :] = 4
        g.grid[-1, :] = 4
        g.grid[:, 0] = 4
        g.grid[:, -1] = 4
        self.assertFalse(self.iswrapcorrect(g))
        g.refresh_wrap()
        self.assertTrue(self.iswrapcorrect(g))

    def test_wrap_edge(self):
        #Test smallest avaliable grid size
        gridshape = 3,3
        self.case(gridshape)

    def test_wrap_valid(self):
        #test larger grid
        gridshape = 20,20
        self.case(gridshape)


#----------------------------------------------------------------------

class TestInitialGridSetMeta(type):
    def __new__(mcs, name, bases, dict):

        def gen_test_array_equal(a,b):
            def test(self):
                self.assertTrue(np.array_equal(a, b))
            return test

        config = CAConfig('test/testdescriptions/2dbasic.py')
        dimensions = 2
        config.states = 0,1,2
        config.nhood_arr = [1,1,1]

        def transfunc(self, grid, neighbourcounts):
            return grid

        #matching dimensions
        config.grid_dims = (20,20)
        testname = "test_gridset_2d_{i}{j}".format(i=config.grid_dims[0], j=config.grid_dims[1])
        config.initial_grid = np.random.randint(0, 3, config.grid_dims)
        g = Grid2D(config, transfunc)
        dict[testname] = gen_test_array_equal(g.grid, config.initial_grid)

        #non matching
        testsize = [(19,20), (20,21), (21,21), (19,19)]
        for s in testsize:
            testname = "test_gridset_2d_{i}{j}".format(i=s[0], j=s[1])
            config.grid_dims = s
            ig = np.random.randint(0, 3, s)
            config.initial_grid = ig
            g = Grid2D(config, transfunc)
            if s < config.grid_dims:
                dict[testname] = gen_test_array_equal(g.grid[:s[0], :s[1]], ig)
            else:
                dict[testname] = gen_test_array_equal(g.grid, ig[:config.grid_dims[0], :config.grid_dims[1]])
        return type.__new__(mcs, name, bases, dict)

class TestInitialGridSet(unittest.TestCase, metaclass=TestInitialGridSetMeta):
    pass

if __name__ == '__main__':
    unittest.main()
