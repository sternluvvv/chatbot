from random import choice , randrange
from janome.tokenizer import Tokenizer
from responder import WhatResponder, RandomResponder, PatternResponder, TemplateResponder #responder.pyからResponderと言う名前のロード(Responder('What')#
from dictionary import Dictionary
import morph

class Unmo:
    def __init__(self,name) :
        self._tokenizer = Tokenizer()
        self._dictionary = Dictionary()
        self._responders = {'what':WhatResponder('What',self._dictionary),'random':RandomResponder('Random',self._dictionary),'pattern':PatternResponder('Pattern',self._dictionary),'template':TemplateResponder('Template',self._dictionary)}    
         #辞書型Whatの中にWhatResponder・・・ Responderクラスに第３因子？が増えた為。Dictionaryクラスをresponder.pyにインポートしなくてもいい代わりに#
        self._name = name
        self._responder = self._responders['pattern'] #Unmoにはself._respondersのpatternキー(PatternResonder)クラスが入ってる#

    def dialogue(self,text) :
        chance = randrange(0,100)
        if chance in range(0,39) :
            self._responder = self._responders['pattern']
        elif chance in range(40,69) :
            self._responder = self._responders['template']
        elif chance in range(70,89) :
            self._responder = self._responders['random']
        else :
            self._responder = self._responders['what']
        
        parts = morph.analyze(text)
        response = self._responder.response(text,parts) #どれかのresponseをresponseとする#
        self._dictionary.study(text,parts) #ないものは記憶させる#
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

    def main() :
        markov = Markov()
        sep = r'[。?？！!   ]+'
        filename = sys.argv[1]
        dicfile = '{}.dat'.format(filename)
        if os.path.exists(dicfile) :
            markov.load(dicfile)

        else :
            with open(filename, encoding = 'utf-8') as f :
                sentences = []
                for line in f :
                    sentences.extend(re.split(sep, line.strip()))
            for sentence in sentenses :
                if sentence :
                    markov.add_sentence(morph.analyze(sentence))
                    print('.',end = '')
                    sys.stdout.flush()
            markov.save(dicfile)
        print('\n')

        while True :
            linr = input('>')
            if not line :
                break
            parts = morph.analyze(line)
            keyword = next((word for word,part in parts if morph.is_keyword(part)),'')

    if __name__ == '__main__' :
        main()
                

