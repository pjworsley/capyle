import sys, inspect, unittest
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('test')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

import numpy as np
from capyle.ca import CAConfig
from capyle.utils import prerun_ca, load
# import capyle.utils as utils

TESTDESCRIPTIONS_PATH = 'test/testdescriptions/'

class TestBasicConfig(unittest.TestCase):
    """
    Test where the dimensions, title and states variables have been explicitly set in the file, but only these values
    """
    def setUp(self):
        x, y = '1dbasic.py','2dbasic.py'
        self.filepath1d = TESTDESCRIPTIONS_PATH + x
        self.filepath2d = TESTDESCRIPTIONS_PATH + y
    def test_basic1d(self):
        ca_config = CAConfig(self.filepath1d)
        self.assertIsInstance(ca_config, CAConfig)
        #values from file
        self.assertEqual(ca_config.title, "Example 1D CA")
        self.assertEqual(ca_config.dimensions, 1)
        #pre run to get states
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertEqual(ca_config.states, (0,1))

    def test_1d_fill(self):
        ca_config = CAConfig(self.filepath1d)
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertIsInstance(ca_config, CAConfig)
        #values from file

        ca_config.fill_in_defaults()
        #values from defaults
        expected_rulenum = 0
        expected_gens = 100
        expected_dims = (expected_gens + 1, expected_gens*2 + 1)
        expected_grid = np.zeros(expected_dims)
        expected_nhood = np.array([1,1,1])
        self.assertEqual(ca_config.rule_num, expected_rulenum)
        self.assertEqual(ca_config.num_generations, expected_gens)
        self.assertEqual(ca_config.grid_dims, expected_dims)
        self.assertTrue(np.array_equal(ca_config.initial_grid, expected_grid))
        self.assertTrue(np.array_equal(ca_config.nhood_arr, expected_nhood))

    def test_basic2d(self):
        ca_config = CAConfig(self.filepath2d)
        self.assertIsInstance(ca_config, CAConfig)
        #values from parsing the file
        self.assertEqual(ca_config.title, "Example 2D CA")
        self.assertEqual(ca_config.dimensions, 2)
        # pre run to get information set by the user
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertEqual(ca_config.title, "Example 2D CA")
        self.assertEqual(ca_config.dimensions, 2)
        self.assertEqual(ca_config.states, (0,1,2))

    def test_2d_fill(self):
        ca_config = CAConfig(self.filepath2d)
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertIsInstance(ca_config, CAConfig)
        #values from file

        ca_config.fill_in_defaults()
        #values from defaults
        expected_rulenum = 0
        # + 1 for generation 0
        expected_gens = 100
        expected_dims = (200, 200)
        expected_grid = np.zeros(expected_dims)
        expected_nhood = np.ones((3,3))
        self.assertEqual(ca_config.rule_num, expected_rulenum)
        self.assertEqual(ca_config.num_generations, expected_gens)
        self.assertEqual(ca_config.grid_dims, expected_dims)
        self.assertTrue(np.array_equal(ca_config.initial_grid, expected_grid))
        self.assertTrue(np.array_equal(ca_config.nhood_arr, expected_nhood))



class TestMinimalConfigComments(unittest.TestCase):
    """
    Test where the descriptor comments have been set,
    and no ca_config variables have been set
    """
    def setUp(self):
        x, y = '1dminimalcoms.py','2dminimalcoms.py'
        self.filepath1d = TESTDESCRIPTIONS_PATH + x
        self.filepath2d = TESTDESCRIPTIONS_PATH + y

    def test_minimal_1d_comments(self):
        ca_config = CAConfig(self.filepath1d)
        #values from file
        self.assertIsInstance(ca_config, CAConfig)
        self.assertEqual(ca_config.title, "Example 1D CA Minimal")
        self.assertEqual(ca_config.dimensions, 1)

    def test_minimal_1d_comments_fill(self):
        ca_config = CAConfig(self.filepath1d)
        self.assertIsInstance(ca_config, CAConfig)
        ca_config.fill_in_defaults()
        #values from defaults
        expected_rulenum = 0
        expected_gens = 100
        # + 1 for generation 0
        expected_dims = (expected_gens + 1, expected_gens*2 + 1)
        expected_grid = np.zeros(expected_dims)
        expected_nhood = np.array([1,1,1])
        self.assertEqual(ca_config.rule_num, expected_rulenum)
        self.assertEqual(ca_config.num_generations, expected_gens)
        self.assertEqual(ca_config.grid_dims, expected_dims)
        self.assertTrue(np.array_equal(ca_config.initial_grid, expected_grid))
        self.assertTrue(np.array_equal(ca_config.nhood_arr, expected_nhood))

    def test_minimal_2d_comments(self):
        #infer data from comments in file
        ca_config = CAConfig(self.filepath2d)
        self.assertIsInstance(ca_config, CAConfig)
        #values from parsing the file
        self.assertEqual(ca_config.title, "Example 2D CA Minimal")
        self.assertEqual(ca_config.dimensions, 2)

    def test_minimal_2d_comments_fill(self):
        ca_config = CAConfig(self.filepath2d)
        self.assertIsInstance(ca_config, CAConfig)
        ca_config.fill_in_defaults()
        #values from defaults
        # + 1 from the inclusion of generation 0
        expected_gens = 100
        expected_dims = (200, 200)
        expected_grid = np.zeros(expected_dims)
        expected_nhood = np.ones((3,3))
        self.assertEqual(ca_config.num_generations, expected_gens)
        self.assertEqual(ca_config.grid_dims, expected_dims)
        self.assertTrue(np.array_equal(ca_config.initial_grid, expected_grid))
        self.assertTrue(np.array_equal(ca_config.nhood_arr, expected_nhood))



class TestMinimalConfigVariables(unittest.TestCase):
    """
    Test where the ca_config variables have been set,
    and no comments have been set
    """
    def setUp(self):
        x, y = '1dminimalvars.py','2dminimalvars.py'
        self.filepath1d = TESTDESCRIPTIONS_PATH + x
        self.filepath2d = TESTDESCRIPTIONS_PATH + y

    def test_minimal_1d_vars(self):
        ca_config = CAConfig(self.filepath1d)
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertIsInstance(ca_config, CAConfig)
        #values from file
        self.assertEqual(ca_config.title, "Example 1D CA Minimal")
        self.assertEqual(ca_config.dimensions, 1)
        #pre run to get states

        self.assertEqual(ca_config.states, (0,1))

    def test_minimal_1d_vars_fill(self):
        ca_config = CAConfig(self.filepath1d)
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertIsInstance(ca_config, CAConfig)
        self.assertEqual(ca_config.states, (0,1))
        #values from file

        ca_config.fill_in_defaults()
        #values from defaults
        expected_rulenum = 0
        expected_gens = 100
        expected_dims = (expected_gens + 1, expected_gens*2 + 1)
        expected_grid = np.zeros(expected_dims)
        expected_nhood = np.array([1,1,1])
        self.assertEqual(ca_config.rule_num, expected_rulenum)
        self.assertEqual(ca_config.num_generations, expected_gens)
        self.assertEqual(ca_config.grid_dims, expected_dims)
        self.assertTrue(np.array_equal(ca_config.initial_grid, expected_grid))
        self.assertTrue(np.array_equal(ca_config.nhood_arr, expected_nhood))

    def test_minimal_2d_vars(self):
        # pre run to get information set by the user
        ca_config = CAConfig(self.filepath2d)
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertEqual(ca_config.title, "Example 2D CA Minimal")
        self.assertEqual(ca_config.dimensions, 2)
        self.assertEqual(ca_config.states, (0,1,2))

    def test_minimal_2d_vars_fill(self):
        ca_config = CAConfig(self.filepath2d)
        prerun_ca(ca_config)
        ca_config = load(ca_config.path)
        self.assertIsInstance(ca_config, CAConfig)
        self.assertEqual(ca_config.states, (0,1,2))
        #values from file
        ca_config.fill_in_defaults()
        #values from defaults
        expected_gens = 100
        expected_dims = (200, 200)
        expected_grid = np.zeros(expected_dims)
        expected_nhood = np.ones((3,3))
        self.assertEqual(ca_config.num_generations, expected_gens)
        self.assertEqual(ca_config.grid_dims, expected_dims)
        self.assertTrue(np.array_equal(ca_config.initial_grid, expected_grid))
        self.assertTrue(np.array_equal(ca_config.nhood_arr, expected_nhood))


class TestNoConfig(unittest.TestCase):
    """
    # Test where no config varibles have been explicitly set and there are no title or dimension comments - infer the title and dimensions from contents of file (eg. from classes called)
    # """

    def setUp(self):
        x, y = '1dnone.py','2dnone.py'
        self.filepath1d = TESTDESCRIPTIONS_PATH + x
        self.filepath2d = TESTDESCRIPTIONS_PATH + y

    def test_1d_none(self):
        ca_config = CAConfig(self.filepath1d)
        self.assertEqual(ca_config.title, "Unamed 1D Automata")
        self.assertEqual(ca_config.dimensions, 1)

    def test_2d_none(self):
        ca_config = CAConfig(self.filepath2d)
        self.assertEqual(ca_config.title, "Unamed 2D Automata")
        self.assertEqual(ca_config.dimensions, 2)

#SET GRID DIMS
class TestGridDimsSetMeta(type):
    def __new__(mcs, name, bases, dict):
        def gen_test_shape_eq(config, x, shape):
            def test(self):
                if (type(x) is tuple):
                    config.set_grid_dims(dims=x)
                else:
                    config.set_grid_dims(num_generations=x)
                self.assertEqual(config.initial_grid.shape, shape)
                self.assertEqual(config.grid_dims, shape)
            return test

        #1d
        #below limit, valid and below current, valid and above current
        gens = [0, 50, 150]
        expected = [(2,3), (51,101), (151, 301)]
        config = CAConfig(TESTDESCRIPTIONS_PATH + "1dbasic.py")
        config.fill_in_defaults()
        for g, e in zip(gens, expected):
            testname = "test_config_setdims_1d_{g}".format(g=g)
            dict[testname] = gen_test_shape_eq(config, g, e)
            dict[testname] = gen_test_shape_eq(config, g, e)

        #2d
        config = CAConfig(TESTDESCRIPTIONS_PATH + "2dbasic.py")
        config.fill_in_defaults()
        shapes = [(2,3), (3,3), (50, 50), (300,300), (300,420)]
        for s in shapes:
            testname = "test_config_setdims_2d_{g}".format(g=g)
            dict[testname] = gen_test_shape_eq(config, s, s)
            dict[testname] = gen_test_shape_eq(config, s, s)

        return type.__new__(mcs, name, bases, dict)

class TestGridDimsSet(unittest.TestCase, metaclass=TestGridDimsSetMeta):
    pass

#SET INITIAL GRID

if __name__ == '__main__':
    unittest.main()
