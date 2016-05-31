import abc
import functools 
import minpy 
from minpy.array_variants import ArrayType
from minpy.core import wraps, minpy_to_numpy

class ParamsNameNotFoundError(ValueError):
    """ Error of not existed name during accessing model params """
    pass

class UnknownAccessModeError(ValueError):
    """ Error of unexpected mode during accessing model params """
    pass


class ModelBase(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self, conv_mode = 'lazy'):
    self.convert_mode = conv_mode
    self.data_target_cnt = 2
    self.params = {}

  def loss(self, features, captions_in_dense, captions_out_dense, mask):
    res = wraps(self.convert_mode)(self.loss_and_derivative)(features, captions_in_dense, captions_out_dense, mask)

    # make loss or score, i.e. res[0], return as numpy.float
    # while grads, i.e. res[1], could be minpy's array
    if (self.convert_mode == 'lazy'):
      if type(res) is not tuple:
        res = minpy_to_numpy(res)
      else:
        return minpy_to_numpy(res[0]), res[1]
    return res

  @abc.abstractmethod
  def loss_and_derivative(self, features, captions_in_dense, captions_out_dense, mask):
    """ do forward and output the loss and derivative, if y is not none"""
    return
