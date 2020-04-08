from random import choice

class Responder :
    
    def __init__(self,name) :
        self._name = name #Responderの名前(変更不可）#

    def response(self,*args) :  #*argsは引数は何でもいい。passは何もしない。(Responder)はけいしょ継承が前提の骨組み
        pass

    @property           #respondername.nameでできる#
    def name(self):
        return self._name

class WhatResponder(Responder):   #って何？のResponder要素ありのクラス#

    def response(self,text) :
        return '{}って何？'.format(text)

class RandomResponder(Responder) : #ランダム返答のResponder要素ありのクラス#
    RESPONSES = ['今日は寒いね','チョコ食べたい','きのう10円拾った']

    def __init__(self,name) :
        self._name = name 

    def response(self,_):  #何がきてもランダムで返答する#
        return choice(RandomResponder.RESPONSES)



#大まかなイメージとしてResponderで返答のバリエーションを作り、#
#UnmoでResponderを入れ、返答するAIをつくる#
#main.pyにはUnmo(Responder付)をいれ返答種類の表示#