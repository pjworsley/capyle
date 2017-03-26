import numpy as np


class Neighbourhood(object):

    def __init__(self, nhood, dims=2):
        """Create a Neighbourhood object for use with the Grid objects"""
        if not (dims == 2 or dims == 1):
            raise ValueError(
                "Unsuported number of dimensions, only 1D or 2D CA supported")
        if dims == 2:
            # 3,3 neighbourhood
            self.neighbourhood = self._prepare2D(nhood)
        else:
            # 3, Neighbourhood
            self.neighbourhood = self._prepare1D(nhood)

    def __str__(self):
        """Return the string version of the neighbourhood array
        when print called on whole object"""
        return np.array_str(self.neighbourhood)

    def _prepare2D(self, nhood):
        """Check the provided neighbourhood is valid and if not
        attempt to make it valid in the unambiguous cases"""
        # check type and if needed convert python list to numpy array
        nhood = self._type_neighbourhood(nhood)
        # check that there are 1 or 2 dimensions
        # we can increase dimensionality, but not reduce
        dimscheck = nhood.ndim == 1 or nhood.ndim == 2
        if not dimscheck:
            raise ValueError(
                "Only 1D or 2D input array supported for a 2D neighbourhood")

        # ensure that the supplied neighbourhood is
        # not empty or has a dimension of 0 in either axis
        arrayempty = (np.array_equal(nhood, np.array([])) or
                      np.array_equal(nhood, np.array([[]])))
        zerodims = (nhood.shape[0] == 0 or
                    (len(nhood.shape) > 1 and nhood.shape[1] == 0))
        if arrayempty or zerodims:
            # set to the empty neighbourhood
            nhood = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])

        # check if the neighbourhood has a center
        if not (self._has_center(nhood)):
            raise ValueError(
                "Neighbourhood must have a center to represent the cell")

        # scale the neighbourhood to the correct size of 3x3
        # [1,1,1] -> [[0,0,0],[1,1,1],[0,0,0]]      #increase
        # nhood.shape = 5,5 -> nhood.shape = 3,3    #decrease
        if nhood.shape > (3, 3):
            print("[WARNING] Neighbourhood too large, scaling to 3x3...")
            nhood = self._reduce_to_3x3(nhood)
        elif nhood.shape < (3, 3):
            nhood = self._increase_to_3x3(nhood)
        return nhood

    def _prepare1D(self, nhood):
        """Validate and prepare a neighbourhood for a 1D CA"""
        nhood = self._type_neighbourhood(nhood)
        dimscheck = nhood.ndim == 1 or nhood.ndim == 2
        if not dimscheck:
            raise ValueError(
                "Only 1D input array supported to create a 2D neighbourhood")
        # check for empty array or a dimension of 0
        if np.array_equal(nhood, np.array([])) or nhood.shape[0] == 0:
            # if either dim is 0 set to empty, but valid neighbourhood
            nhood = np.array([0, 1, 0])
        # handle empty array
        if nhood.shape == (1,):
            nhood = np.array([0, nhood[0], 0])
        # handle any erronous or 2d input array
        if not (len(nhood.shape) == 1):
            raise ValueError("Neighbourhood must be 1D eg. [1, 0, 1]")
        # handle any even proportioned arrays
        if not (self._has_center(nhood)):
            raise ValueError(
                "Neighbourhood must have a center to represent the cell")
        return nhood

    def _has_center(self, nhood):
        """Returns true if the shape of the neighbourhood is odd
        and hence has a center cell"""
        shape = nhood.shape
        if shape == (1, 1):
            # Single entry
            return True
        if len(shape) == 1 and shape[0] % 2 == 1:
            # 1D array with center
            return True
        if len(shape) == 2 and shape[0] % 2 == 1 and shape[1] % 2 == 1:
            # 2D array with center
            return True
        return False

    def _reduce_to_3x3(self, nhood, fullmatrix=True):
        """
        With the fullmatrix == True, the array will be reduced to 3x3,
        otherwise the appropriate dimensions will be reduced
        eg. [[1,1,1,1,1]] -> [[1,1,1]]
        """
        rows, cols = nhood.shape
        if fullmatrix and (rows == cols == 3):
            return nhood
        elif not fullmatrix and cols <= 3 and rows <= 3:
            return nhood
        if rows > 3:
            nhood = nhood[1:-1]
        if cols > 3:
            nhood = nhood[:, 1:-1]
        return self._reduce_to_3x3(nhood, fullmatrix)

    def _increase_to_3x3(self, nhood):
        # Only valid shapes at this point either have a 3 or 1
        # If one dimension greater than 3 then reduce to 3
        if any(s > 3 for s in nhood.shape):
            nhood = self._reduce_to_3x3(nhood, fullmatrix=False)

        new_col = np.zeros((3, 1))
        new_row = np.zeros((3))

        if nhood.shape == (1, 3):
            nhood = nhood[0]
            shape = nhood.shape
        if nhood.shape == (3,):
            nhood = np.vstack((nhood, new_row))
            nhood = np.vstack((new_row, nhood))
            return nhood

        if nhood.shape == (3, 1):
            nhood = np.hstack((nhood, new_col))
            nhood = np.hstack((new_col, nhood))
            return nhood

        if nhood.shape == (1,) or nhood.shape == (1, 1):
            return np.zeros((3, 3))

    def _type_neighbourhood(self, nhood):
        """Checks the type of the neighbourhood provided
        allows list or np.ndarray, rejects others"""
        nhoodtype = type(nhood)
        if not (nhoodtype is np.ndarray or nhoodtype is list):
            raise TypeError(
                "Neighbourhood must be created with a list or numpy array")
        # if list turn into numpy.ndarray
        if nhoodtype == list:
            return np.array(nhood)
        # else return numpy array
        return nhood
