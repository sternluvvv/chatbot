import re #正規表現#
from janome.tokenizer import Tokenizer #形態素解析#
class Dictionary :

    DICT_RANDOM = 'random.txt'
    DICT_PATTERN = 'pattern.txt'
    TOKENIZER = Tokenizer()

    def __init__(self):
        with open(Dictionary.DICT_RANDOM, encoding = 'utf-8')as f :  #random.txtで1行ごと読みとる#
            self._random = [x for x in f.read().splitlines() if x]

        
        with open(Dictionary.DICT_PATTERN, encoding = 'utf-8') as f :  #pattern.txtで1行ごとかつtabで分ける#
            self._pattern = [Dictionary.make_pattern(l) for l in f.read().splitlines() if l]    #fを1行ごと改行し、lとする。もしlがあれば、make_patternでpatternとphrases#
                                                                                                   # にわける#

    @property
    def random(self) :
        return self._random #上で開いたtext#
    
    @property
    def pattern(self) : #上でpattern とphrasesに分けている#
        return self._pattern

    def study(self,text) :
        self.study_random(text)
        self.study_pattern(text, Dictionary.analyze(text))

    def study_random(self, text) :
        if not text in self._random :
            self._random.append(text)  #もし打った言葉がrandom.txtに無ければ追加#

    def study_pattern(self, text , parts) : #partsとはDictionary.analyze(text)でsurfaceとpartに1行ごと分れている#
        for word , part in parts :      
            if self.is_keyword(part) :      #もしpartに名詞があれば(True)以下を行う#
                duplicated = next((p for p in self._pattern if p['pattern'] == word),None)
                                            #self._pattern(pattern[tab]phrases)を1行ずつ読みpとする、もしpのpattenにsurfaceがあれば、そのpatternをかえす#
                if duplicated :             #もしpatternがあった場合以下を行う#
                    if not text in duplicated['phrases'] :　#もしpのphrasesにtextがなければprasesを追加#
                        duplicated['phrases'].append(text)
                else :                                      #もし全てなければ新しいパターンの追加
                    self._pattern.append({'pattern':word,'phrases':[text]})


    def save(self):
        with open(Dictionary.DICT_RANDOM, mode='w',encoding='utf-8') as f : #txtの書き込みする引数w#
            f.write('\n'.join(self.random)) #f(random.txt)に\nしながらslf.randomを書き込む#

        with open(Dictionary.DICT_PATTERN, mode='w', encoding='utf-8') as f:
            f.write('\n'.join([Dictionary.pattern_to_line(p) for p in self._pattern]))

    @staticmethod
    def analyze(text) :
        return [(t.surface, t.part_of_speech) for t in Dictionary.TOKENIZER.tokenize(text)]
                        #textを形態素解析して1行ごとに読み、(surface,parts)のかたちにして改行されていく#
    
    @staticmethod
    def pattern_to_line(pattern) :
        return '{}\t{}'.format(pattern['pattern'],'|'.join(pattern['phrases'])) #pattern /t phrase|phrase|phrase#

    @staticmethod
    def is_keyword(part) :
        return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)',part)) #boolは真偽値。partと名詞の部類がマッチすればtrueを返す。他の品詞の場合だめ#

    @staticmethod
    def make_pattern(line) :        #pattern辞書が入ることを予測#
        pattern, phrases = line.split('\t')     #patternとphrasesをタブでわける#
        if pattern and phrases :            #もしpattern と　phrasesがあれば#
            return {'pattern': pattern, 'phrases':phrases.split('|')} #patten : pattern phrases : phrase|phrase となる#