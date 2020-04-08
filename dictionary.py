class Dictionary :

    DICT_RANDOM = 'random.txt'
    DICT_PATTERN = 'pattern.txt'

    def __init__(self):
        with open(Dictionary.DICT_RANDOM, encoding = 'utf-8')as f :  #random.txtで1行ごと良いとる#
            self._random = [x for x in f.read().splitlines() if x]

        self._pattern = []
        with open(Dictionary.DICT_PATTERN, encoding = 'utf-8') as f :  #pattern.txtで1行ごとかつtabで分ける#
            for line in f :
                pattern, phrases = line.strip().split('\t')
                if pattern and phrases :
                    self._pattern.append({'pattern': pattern,'phrases':phrases})

    @property
    def random(self) :
        return self._random
    
    @property
    def pattern(self) : #上でpattern とphrasesに分けている#
        return self._pattern
