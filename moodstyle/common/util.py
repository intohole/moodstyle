#encoding=utf-8

from b2 import exceptions2


def entropy(probs):
    """calc entropy
        :param:probs:probality array:float array
        :return:entropy:float
    """
    exceptions2.judge_null(probs)
    if isinstance(probs, (list, tuple)):
        return sum([-prob * log(prob, 2) for prob in probs])
    elif isinstance(probs, (int, float)):
        return -probs * log(probs, 2)
