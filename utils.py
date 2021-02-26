from collections import namedtuple
import pickle
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np
from gym_board import GymBoard
from collections import OrderedDict

Step = namedtuple("Step", ["matrix", "action", "action_encoded"])
Game = namedtuple("Game", ["steps", "score", "random_seed", "is_gameover"])

actions = list(range(GymBoard.NB_ACTIONS))


def save_history(history, file):
    with open(file, mode="bw") as f:
        pickle.dump(history, f)


def get_callback(callbacks, callback_class):
    class CallbackNotFound(Exception):
        pass

    callback = [x for x in callbacks if isinstance(x, callback_class)]
    if callback:
        callback = callback[0]
        callback.model = None
        callback.params = None
        return callback
    else:
        raise CallbackNotFound("Instance of {} not found.".format(callback_class))


def train_test_stratified(X, y, test_size=0.3):
    """
    Split the data to train-test sets so there are same amounts of classes.

    Parameters
    ----------
    X
    y
    test_size

    Returns
    -------
    tuple(list, list)
        Indexes of train and test data.
    """

    i_list = np.array(list(StratifiedShuffleSplit(test_size=test_size).split(X, y)))
    id = np.random.choice(len(i_list), 1)
    train_i = i_list[id][0][0]
    test_i = i_list[id][0][1]
    return train_i, test_i

def encode_action(action):
    if action == 0:
        return np.array([1, 0, 0, 0])
    elif action == 1:
        return np.array([0, 1, 0, 0])
    elif action == 2:
        return np.array([0, 0, 1, 0])
    elif action == 3:
        return np.array([0, 0, 0, 1])
