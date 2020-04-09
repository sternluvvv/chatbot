import re       #正規表現#
from random import choice

class Responder :
    
    def __init__(self,name,dictionary) : #dictionaryの追加でDictionaryを追加しなくていい#
        self._name = name #Responderの名前(変更不可）#
        self._dictionary = dictionary

    def response(self,*args) :  #*argsは引数は何でもいい。passは何もしない。(Responder)はけいしょ継承が前提の骨組み
        pass

    @property           #respondername.nameでできる#
    def name(self):
        return self._name

class WhatResponder(Responder):   #って何？のResponder要素ありのクラス#

    def response(self,text) :
        return '{}って何？'.format(text)

class RandomResponder(Responder) : #ランダム返答のResponder要素ありのクラス#

    def response(self,_):  #何がきてもランダムで返答する#
        return choice(self._dictionary.random)

class PatternResponder(Responder) : #PatternResponderクラスを作る#

    def response(self, text) :
        for ptn in self._dictionary.pattern : #pattern.txtの中身をptternでパースした後の1行#
            matcher = re.search(ptn['pattern'],text) 
            if matcher :    #もし、patternの方とresponseの打つ文字（text）の中身がマッチした場合#
                chosen_response = choice(ptn['phrases'])    #phrasesの方のいずれかを選ぶ#
                return chosen_response.replace('%match%',matcher[0]) #%match%と打った文字(text)で合っているものを交換#
        return choice(self._dictionary.random)      #その他はrandom.txtからチョイス#




#大まかなイメージとしてResponderで返答のバリエーションを作り、#
#UnmoでResponderを入れ、返答するAIをつくる#
#main.pyにはUnmo(Responder付)をいれ返答種類の表示#