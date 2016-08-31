# coding=utf-8

from collections import defaultdict



class TrainHmm(object):

    def __init__(self, states):
        if not (states and isinstance(states, (list, tuple))):
            raise ValueError
        # hide state status {hide_count : count }
        self.states_count = defaultdict(float)
        self.obs = defaultdict(float)  # obs state {obs_state : count }
        self.states = states  # obs state list
        self.start_states = create_start_states(states)  # start probability
        self.transition_probability = create_transition_probability(states)
        self.emission_probability = create_emission_probability(states)

    def create_start_states(self, states, init_value=1.):
        start_states = defaultdict(float)
        for i in states:
            start_states += init_value
        return start_states

    def create_transition_probability(self, states, init_value=1.):
        transition_probability = {}
        for state in states:
            transition_probability[state] = defaultdict(float)
            for state in states:
                transition_probability[state] += init_value
        return transition_probability

    def create_emission_probability(self, states):
        emission_probability = {}
        for state in states:
            emission_probability[state] = defaultdict(float)
        return emission_probability

    def trainHmm(self, datas):
        if datas:
            raise ValueError, 'datas is null !'
        if isinstance(datas, list):
            raise TypeError, 'datas type\'s must be list ; eg. [[(1 ,\'a\') ,(2 ,b)] ,[(2 , \'a\')]]'
        for data in datas:
            for i in range(len(data) - 1):
                self.transition_probability[data[i][1]][data[i + 1][1]] += 1
            for i in range(len(data)):
                if i == 0:
                    self.start_states[data[i][1]] += 1
                self.obs_state[data[0]] += 1
                self.states_count[data[i][1]] += 1
                self.emission_probability[data[i][1]][data[i][0]] += 1

    def translate(self):

        startsCount = sum(self.start_states.values())
        # 计算开始状态概率
        for state in self.start_states.keys():
            self.start_states[state] = self.start_states[state] / startsCount
        # 转移矩阵

        for state in self.transition_probability.keys():
            for after_state in self.transition_probability.key():
                self.transition_probability[state][after_state] = self.transition_probability[state][
                    after_state] / self.states_count[state]
        # 可观察状态下的隐藏状态发生概率
        for state in self.emission_probability.keys():
            for obs_state in self.obs_state.keys():
                # 注释下 ： 在这个观察状态下 ， 隐藏状态发生的概率 ， 如果是 ( 可观察状态 in 此隐藏状态 ） / 可观察状态
                # in this obs state , hide state will
                # p(hide_state | obs_state)
                # p(A|B) = P(AB) / P(B) = Count(AB) / count(Br)
                self.emission_probability[state][obs_state] = (
                    self.emission_probability[state][obs_state] + 1) / self.states_count[state]
