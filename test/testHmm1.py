# coding=utf-8
'''

'''






from collections import defaultdict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from cPickle import load
from cPickle import dump

class HmmItem(object):

    __slots__ = ('obs', 'hide')

    def __init__(self, obs, hide):
        self.obs = obs
        self.hide = hide

    def __str__(self):
        return 'obs_state: %s \t hide_state: %s' % (self.obs, self.hide)


class HmmItems(list):

    '''
    主要为了存储序列性观察与隐藏相对应状态 ；
    主要方法：
    t[1]=(1,2)
    t.append(HmmItem) or t.append((obs , hide))
    '''

    def __check(self, value):
        if not value:
            raise ValueError, 'value is nothing , keep it out'

    def __setitem__(self, key, value):
        self.__check(value)
        if isinstance(value, HmmItem):
            super(HmmItems, self).__setitem__(key, value)
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            super(HmmItems, self).__setitem__(key, HmmItem(value[0], value[1]))
        else:
            raise TypeError, 'HmmItems append accept type only ( HmmItem , tuple or list which is first item is obs state and second is hide state!) '

    def append(self, value):
        self.__check(value)
        if isinstance(value, HmmItem):
            super(HmmItems, self).append(value)
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            super(HmmItems, self).append(HmmItem(value[0], value[1]))
        else:
            raise TypeError, 'HmmItems append accept type only ( HmmItem , tuple or list which is first item is obs state and second is hide state!) '

    def __str__(self):
        return ' '.join(['%s' % str(i) for i in self])

class HmmModel(object):

    def __init__(self, states):
        if not (states and isinstance(states, (list, tuple))):
            raise ValueError
        self.states_count = defaultdict(float)
        self.obs_state = defaultdict(float)  # obs state {obs_state : count }
        self.states = states  # obs state list
        self.start_states = self.create_start_states(states)  # start probability
        self.transition_probability = self.create_transition_probability(states)
        self.emission_probability = self.create_emission_probability(states)

    def create_start_states(self, states, init_value=1.):
        start_states = defaultdict(float)
        for state in states:
            start_states[state] += init_value
        return start_states

    def create_transition_probability(self, states, init_value=1.):
        transition_probability = {}
        for state in states:
            transition_probability[state] = defaultdict(float)
            for after_state in states:
                transition_probability[state][after_state] += init_value
        return transition_probability

    def create_emission_probability(self, states):
        emission_probability = {}
        for state in states:
            emission_probability[state] = defaultdict(float)
        return emission_probability




class Hmm(object):

    def __init__(self, model_path):
        model = self.load(model_path)
        if model and isinstance(model, HmmModel):
            self.model = model
        else:
            raise TypeError, 'model file not have right hmm model!  : %s' % model_path

    def load(self, model_path):
        with open(model_path, 'rb') as f:
            return load(f)

    def viterbi(self, obs):
        '''
        特比算法 摘自wiki 维特比算法
        '''
        V = [{}]
        path = {}
        for y in self.model.states:
            V[0][y] = self.model.start_states[y] * \
                self.model.emission_probability[y][obs[0]]
            path[y] = [y]
        for t in range(1, len(obs)):
            V.append({})
            newpath = {}
            for y in self.model.states:
                (prob, state) = max(
                    [(V[t - 1][y0] * self.model.transition_probability[y0][y] * self.model.emission_probability[y][obs[t]], y0) for y0 in self.model.states])
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath
        (prob, state) = max([(V[len(obs) - 1][y], y)
                             for y in self.model.states])
        return (prob, path[state])


class TrainHmm(object):

    def __init__(self, states):
        self.hmm = HmmModel(states)

    def save(self, model_path):
        with open(model_path, 'wb') as f:
            dump(self.hmm, f)

    def add_item(self, hmmitems):

        for i in range(len(hmmitems) - 1):
            self.hmm.transition_probability[hmmitems[i].hide][
                hmmitems[i + 1].hide] += 1
        self.hmm.start_states[hmmitems[0].hide] += 1
        for item in hmmitems:
            self.hmm.obs_state[item.obs] += 1
            self.hmm.states_count[item.hide] += 1
            self.hmm.emission_probability[item.hide][item.obs] += 1

    def translate(self):

        startsCount = sum(self.hmm.start_states.values())
        # 计算开始状态概率
        for state in self.hmm.start_states.keys():
            self.hmm.start_states[state] = self.hmm.start_states[
                state] / startsCount
        # 转移矩阵
        hide_state_keys = self.hmm.transition_probability.keys()
        for hide_state in hide_state_keys:
            for after_hide_state in hide_state_keys:
                self.hmm.transition_probability[hide_state][after_hide_state] = self.hmm.transition_probability[hide_state][
                    after_hide_state] / self.hmm.states_count[hide_state]
        # 可观察状态下的隐藏状态发生概率
        for hide_state in self.hmm.emission_probability.keys():
            for obs_state in self.hmm.obs_state.keys():
                # 注释下 ： 在这个观察状态下 ， 隐藏状态发生的概率 ， 如果是 ( 可观察状态 in 此隐藏状态 ） / 可观察状态
                # in this obs state , hide state will
                # p(hide_state | obs_state)
                # p(A|B) = P(AB) / P(B) = Count(AB) / count(Br)
                self.hmm.emission_probability[hide_state][obs_state] = (
                    self.hmm.emission_probability[hide_state][obs_state] + 1.) / self.hmm.states_count[hide_state]


if __name__ == '__main__':
    import os
    import re
    t = Hmm('d:/model.bin')
    print t.viterbi(u'我')

    # t = TrainHmm(['s' , 'b' ,'m' ,'e'])
    # import codecs

    # word_split = re.compile('/[a-z]+ ?')
    # diff = set()
    # chinese = 'd:/data/chinese/'
    # hmmItems = HmmItems()
    # for file_name in os.listdir(chinese):
    #     file_path = '%s%s' % (chinese, file_name)
    #     with open(file_path) as f:
    #         content = f.readlines()
    #     try:
    #         wd = content[2].split('：')[1].strip()
    #     except Exception, e:
    #         print file_path, e
    #         continue
    #     print 'read file %s , read line %s' % (file_path  , len(content))
    #     for line in content[6:]:
    #         line = line.strip().replace(' [%s]' % wd, wd).replace(
    #             ' [%s] ' % wd, wd).replace('[%s] ' % wd, wd).split("\t")[2]
    #         if line in diff:
    #             continue
    #         diff.add(line)
    #         del hmmItems[:]
    #         hmmItems = HmmItems()
    #         line = line.decode('utf-8')
    #         words = word_split.split(line.strip())
    #         for word in words:
    #             # word = word.decode('utf-8')  # 因为汉字是utf-8
    #             word = word.strip()
    #             if len(word) == 1:
    #                 hmmItems.append((word, 's'))
    #             elif len(word) == 2:
    #                 hmmItems.append((word[0], 'b'))
    #                 hmmItems.append((word[1], 'e'))
    #             elif len(word) > 2:
    #                 hmmItems.append((word[0], 'b'))
    #                 for mid_word in word[1:-1]:
    #                     hmmItems.append((mid_word, 'm'))
    #                 hmmItems.append((word[-1], 'e'))
    #         if len(hmmItems) == 0 :
    #             continue
    #         t.add_item(hmmItems)
    # t.translate()
    # t.save('d:/model.bin')
