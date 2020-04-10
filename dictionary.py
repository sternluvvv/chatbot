import os.path
from collections import defaultdict
import morph

class Dictionary :
    DICT = {'random':'random.txt','pattern':'pattern.txt','template':'template.txt'}

    def __init__(self):
        Dictionary.touch_dics()
        with open(Dictionary.DICT['random'], encoding = 'utf-8')as f :  #random.txtで1行ごと読みとる#
            self._random = [x for x in f.read().splitlines() if x]

        
        with open(Dictionary.DICT['pattern'], encoding = 'utf-8') as f :  #pattern.txtで1行ごとかつtabで分ける#
            self._pattern = [Dictionary.make_pattern(l) for l in f.read().splitlines() if l]    #fを1行ごと改行し、lとする。もしlがあれば、make_patternでpatternとphrases#
                                                                                                   # にわける#
        with open(Dictionary.DICT['template'],encoding='utf-8') as f :
            self._template = defaultdict(lambda:[],{}) #txtにない場合デフォルト値を[]とし,表示。#
            for line in f :
                count , template = line.strip().split('\t') #1行をcount templateにわける#
                if count and template :
                    count = int(count)  #countは整数#
                    self._template[count].append(template)  #辞書作成count : template tenplateとなっていく#

    @staticmethod
    def touch_dics() :
        for dic in Dictionary.DICT.values() : 
            if not os.path.exists(dic): #もしdicにファイルやテキストが存在しなければ#
                    open(dic, 'w').close()  #w 書き込みモード：同名のファイルが存在する場合はそのファイルに上書き。存在しない場合は新規作成。#

    @property
    def random(self) :
        return self._random #上で開いたtext#
    
    @property
    def pattern(self) : #上でpattern とphrasesに分けている#
        return self._pattern
    
    @property
    def template(self):
        return self._template

    def study(self,text,parts) :
        self.study_random(text)
        self.study_pattern(text, parts)
        self.study_template(parts)

    def study_random(self, text) :
        if not text in self._random :
            self._random.append(text)  #もし打った言葉がrandom.txtに無ければ追加#

    def study_pattern(self, text , parts) : #partsとはDictionary.analyze(text)でsurfaceとpartに1行ごと分れている#
        for word , part in parts :      
            if morph.is_keyword(part) :      #もし形態素解析の結果に名詞があれば(True)以下を行う#
                duplicated = next((p for p in self._pattern if p['pattern'] == word),None)
                                            #self._pattern(pattern[tab]phrases)を1行ずつ読みpとする、もしpのpattenに読み取った名詞があれば、そのpatternをかえす#
                if duplicated :             #もしpattern(名詞)があった場合以下を行う#
                    if not text in duplicated['phrases'] :  #もし名詞があってもフレーズが無ければprasesを追加#
                        duplicated['phrases'].append(text)
                else :                                      #もし全てなければ新しいパターンの追加
                    self._pattern.append({'pattern':word,'phrases':[text]})

    def study_template(self, parts) :
        template = ''
        count = 0
        for word , part in parts :  #surface partにわかれている#
            if morph.is_keyword(part):  #もしpart(形態素解析された品詞)に名詞があれば#
                word = '%noun%'         #名詞は%noun%にかわる#
                count += 1          
            template += word #templateには元のwordをきろく#

        if count > 0 and template not in self._template[count] : #'%noun%'がひとつ以上あり、テンプレートが既存のものでなければ辞書に追加します#
            self._template[count].append(template)          #辞書にcount : templateを新しく追加#


    def save(self):
        with open(Dictionary.DICT['random'], mode='w',encoding='utf-8') as f : #txtの書き込みする引数w#
            f.write('\n'.join(self.random)) #f(random.txt)に\nしながらslf.randomを書き込む#

        with open(Dictionary.DICT['pattern'], mode='w', encoding='utf-8') as f:
            f.write('\n'.join([Dictionary.pattern_to_line(p) for p in self._pattern]))
        
        with open(Dictionary.DICT['template'], mode = 'w',encoding='utf-8') as f :
            for count , templates in self._template.items() : #items()は要素ふたつとも返す。#
                for template in templates : #いる？#
                    f.write('{}\t{}\n'.format(count,template))

   
    @staticmethod
    def pattern_to_line(pattern) :
        return '{}\t{}'.format(pattern['pattern'],'|'.join(pattern['phrases'])) #pattern /t phrase|phrase|phrase#

    @staticmethod
    def make_pattern(line) :        #pattern辞書が入ることを予測#
        pattern, phrases = line.split('\t')     #patternとphrasesをタブでわける#
        if pattern and phrases :            #もしpattern と　phrasesがあれば#
            return {'pattern': pattern, 'phrases':phrases.split('|')} #patten : pattern phrases : phrase|phrase となる#