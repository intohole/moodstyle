# coding=utf-8


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



    def __check(self , value):
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



    def add_item(self , hmmitems):

        for i in range(len(hmmitems[:-1]) - 1) :
            self.transition_probability[hmmitems[i].hide][hmmitems[i + 1].hide] += 1
        self.start_states[hmmitems[0].hide] += 1
        for item in hmmitems:
            self.obs_state[item[i].obs] += 1
            self.states_count[item[i].hide] += 1
            self.emission_probability[item.hide][item.obs] += 1



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


if __name__ == '__main__':
    a = []
    a.append('a')
    t = HmmItems()
    t.append((1, 2))
    print t
