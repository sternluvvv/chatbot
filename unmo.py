from random import choice
from responder import WhatResponder, RandomResponder, PatternResponder #responder.pyからResponderと言う名前のロード(Responder('What')#
from dictionary import Dictionary

class Unmo:
    def __init__(self,name) :
        self._dictionary = Dictionary()
        self._responders = {'What':WhatResponder('What',self._dictionary),'Random':RandomResponder('Random',self._dictionary),'pattern':PatternResponder('Pattern',self._dictionary),}    
         #辞書型Whatの中にWhatResponder・・・ Responderクラスに第３因子？が増えた為。Dictionaryクラスをresponder.pyにインポートしなくてもいい代わりに#
        self._name = name
        self._responder = self._responders['pattern'] #Unmoにはself._respondersのpatternキー(PatternResonder)クラスが入ってる#

    def dialogue(self,text) :
        chosen_key = choice(list(self._responders.keys())) #辞書のキーをlistにして、えらぶ#
        self._responder = self._responders[chosen_key] #下のself._responderをランダムに選ぶ#
        return self._responder.response(text) #RandomResponder or WhatResponderのresponseをもってきた#

    @property
    def name(self) :
        return self._name

    @property
    def responder_name(self):
        return self._responder.name #Randomとでるはず#

