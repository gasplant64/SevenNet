import os.path

import torch

from sevenn.nn.activation import ShiftedSoftPlus
import sevenn._keys as KEY
from typing import Dict, Any

SEVENN_VERSION = "0.90"
IMPLEMENTED_RADIAL_BASIS = ['bessel']
IMPLEMENTED_CUTOFF_FUNCTION = ['poly_cut']

IMPLEMENTED_MODEL = ['E3_equivariant_model']

# string input to real torch function
ACTIVATION_FOR_EVEN = {"ssp": ShiftedSoftPlus, "silu": torch.nn.functional.silu}
ACTIVATION_FOR_ODD = {"tanh": torch.tanh, "abs": torch.abs}
ACTIVATION_DICT = {"e": ACTIVATION_FOR_EVEN, "o": ACTIVATION_FOR_ODD}
# to avoid torch script to compile torch_geometry.data
AtomGraphDataType = Dict[str, torch.Tensor]


def is_dir_avail(x):
    return type(x) is str and os.path.isdir(os.path.dirname(x))


def is_file(x):
    return type(x) == str and os.path.isfile(x)


def is_positive(x):
    return x > 0


def is_list_of_file_or_file(x):
    if type(x) is str:
        x = [x]
    return all([os.path.isfile(v) for v in x])


DEFAULT_E3_EQUIVARIANT_MODEL_CONFIG = {
    KEY.NODE_FEATURE_MULTIPLICITY: 32,
    KEY.LMAX: 1,
    KEY.IS_PARITY: True,
    KEY.RADIAL_BASIS: {
        KEY.RADIAL_BASIS_NAME: 'bessel',
        KEY.BESSEL_BASIS_NUM: 8,
    },
    KEY.CUTOFF_FUNCTION: {
        KEY.CUTOFF_FUNCTION_NAME: 'poly_cut',
        KEY.POLY_CUT_P: 6,
    },

    KEY.CUTOFF: 4.5,
    KEY.NUM_SPECIES: 2,  # remove later
    KEY.CONVOLUTION_WEIGHT_NN_HIDDEN_NEURONS: [64, 64],
    KEY.NUM_CONVOLUTION: 2,
    KEY.ACTIVATION_SCARLAR: {"e": "silu", "o": "tanh"},
    KEY.ACTIVATION_GATE: {"e": "silu", "o": "tanh"},
    KEY.AVG_NUM_NEIGHBOR: True,
}


DEFAULT_DATA_CONFIG = {
    KEY.DTYPE: "single",
    KEY.FORMAT_OUTPUTS: 'vasp-out',
    KEY.STRUCTURE_LIST: False,
    KEY.SAVE_DATASET: 'saved_dataset.pt',
    KEY.LOAD_DATASET: False,
    KEY.RATIO: 0.1,
    KEY.BATCH_SIZE: 6,
}


DEFAULT_TRAINING_CONFIG = {
    KEY.RANDOM_SEED: 1,
    KEY.EPOCH: 300,
    KEY.OPTIMIZER: 'adam',
    KEY.SCHEDULER: 'exponentiallr',
    KEY.FORCE_WEIGHT: 0.1,
    KEY.SKIP_OUTPUT_UNTIL: 20,
    KEY.OUTPUT_PER_EPOCH: 10,  # False or positive integer
    KEY.DRAW_LC: True,
    KEY.DRAW_PARITY: True,
    KEY.USE_TESTSET: False,
    KEY.CONTINUE: None,
    KEY.NUM_WORKERS: 0,

    KEY.OUTPUT_PER_EPOCH: {
        KEY.PER_EPOCH: 30,
        KEY.DRAW_PARITY: False,
        KEY.MODEL_CHECK_POINT: True,
        KEY.DEPLOY_MODEL: True,
        KEY.SAVE_DATA_PICKLE: False,
    }
}


# condition for each inputs, key omitted here should be initialized by hand
MODEL_CONFIG_CONDITION = {
    KEY.NODE_FEATURE_MULTIPLICITY: is_positive,
    KEY.LMAX: is_positive,
    KEY.IS_PARITY: None,
    KEY.RADIAL_BASIS: {
        KEY.RADIAL_BASIS_NAME: lambda x: x in IMPLEMENTED_RADIAL_BASIS,
        KEY.BESSEL_BASIS_NUM: is_positive,
    },
    KEY.CUTOFF_FUNCTION: {
        KEY.CUTOFF_FUNCTION_NAME: lambda x: x in IMPLEMENTED_CUTOFF_FUNCTION,
        KEY.POLY_CUT_P: is_positive,
    },
    KEY.CUTOFF: is_positive,
    KEY.NUM_CONVOLUTION: is_positive,
    KEY.CONVOLUTION_WEIGHT_NN_HIDDEN_NEURONS:
        lambda x: all(val > 0 and isinstance(val, int) for val in x),
    KEY.AVG_NUM_NEIGHBOR: None,
}


DATA_CONFIG_CONDITION = {
    KEY.DTYPE: lambda x: x.lower() in ["single", "double"],
    KEY.FORMAT_OUTPUTS: lambda x: x in ["vasp-out"],
    KEY.SAVE_DATASET: None,
    KEY.RATIO: lambda x: type(x) is float and x > 0.0 and x < 0.5,
    KEY.BATCH_SIZE: is_positive,
}

TRAINING_CONFIG_CONDITION = {
    KEY.RANDOM_SEED: is_positive,
    KEY.EPOCH: is_positive,
    KEY.FORCE_WEIGHT: is_positive,
    KEY.SKIP_OUTPUT_UNTIL: is_positive,
    KEY.DRAW_LC: None,
    KEY.DRAW_PARITY: None,
    KEY.USE_TESTSET: None,
    KEY.NUM_WORKERS: is_positive,
    KEY.OUTPUT_PER_EPOCH: {
        KEY.PER_EPOCH: lambda x: is_positive(x) or x is False,
        KEY.DRAW_PARITY: None,
        KEY.MODEL_CHECK_POINT: None,
        KEY.DEPLOY_MODEL: None,
        KEY.SAVE_DATA_PICKLE: None,
    },
    KEY.CONTINUE: None,
}
