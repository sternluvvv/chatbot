from random import choice , randrange
from responder import WhatResponder, RandomResponder, PatternResponder #responder.pyからResponderと言う名前のロード(Responder('What')#
from dictionary import Dictionary

class Unmo:
    def __init__(self,name) :
        self._dictionary = Dictionary()
        self._responders = {'what':WhatResponder('What',self._dictionary),'random':RandomResponder('Random',self._dictionary),'pattern':PatternResponder('Pattern',self._dictionary),}    
         #辞書型Whatの中にWhatResponder・・・ Responderクラスに第３因子？が増えた為。Dictionaryクラスをresponder.pyにインポートしなくてもいい代わりに#
        self._name = name
        self._responder = self._responders['pattern'] #Unmoにはself._respondersのpatternキー(PatternResonder)クラスが入ってる#

    def dialogue(self,text) :
        chance = randrange(0,100)
        if chance in range(0,59) :
            self._responder = self._responders['pattern']
        elif chance in range(60,89) :
            self._responder = self._responders['random']
        else :
            self._responder = self._responders['what']
        
        response = self._responder.response(text) #どれかのresponseをresponseとする#
        self._dictionary.study(text) #ないものは記憶させる#
        return response

                # chosen_key = choice(list(self._responders.keys()))これに確率をつけたのが上 #辞書のキーをlistにして、えらぶ#
                #self._responder = self._responders[chosen_key] #下のself._responderをランダムに選ぶ#
        
    def save(self):
        self._dictionary.save()


    @property
    def name(self) :
        return self._name

    @property
    def responder_name(self):
        return self._responder.name #Randomとでるはず#

