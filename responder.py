import re       #正規表現#
from random import choice
import morph

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

    def response(self,text,_) :
        return '{}って何？'.format(text)

class RandomResponder(Responder) : #ランダム返答のResponder要素ありのクラス#

    def response(self,*args):  #何がきてもランダムで返答する#
        return choice(self._dictionary.random)

class PatternResponder(Responder) : #PatternResponderクラスを作る#

    def response(self, text,_) :
        for ptn in self._dictionary.pattern : #pattern.txtの中身をptternでパースした後の1行#
            matcher = re.search(ptn['pattern'],text) 
            if matcher :    #もし、patternの方とresponseの打つ文字（text）の中身がマッチした場合#
                chosen_response = choice(ptn['phrases'])    #phrasesの方のいずれかを選ぶ#
                return chosen_response.replace('%match%',matcher[0]) #%match%と打った文字(text)で合っているものを交換#
        return choice(self._dictionary.random)      #その他はrandom.txtからチョイス#

class TemplateResponder(Responder) :    #%noun%の数が一致するものを返す？#
    def response(self, _,parts):
        keywords = [word for word, part in parts if morph.is_keyword(part)]  #打った文字に対してwordは品詞partは形態素解析の結果で名詞だけリストする#
        count = len(keywords)   #keyword(word)名詞の数が一つでもある場合以下を行う#
        if count > 0 :
            if count in self._dictionary.template : # template辞書に同じ数があれば#
                template = choice(self._dictionary.template[count]) #countが同じものの中からフレーズを選ぶ#
                for keyword in keywords : #名詞リストから一つずつ以下の式で返す#
                    template = template.replace('%noun%',keyword,1) #選んだフレーズの%noun%とkeywordを1つずつ交換する#
                return template #交換したものを返す#
        return choice(self._dictionary.random)  #count=0か指定されたテンプレートがなかった場合はrandom.txtから選んでかえす#





#大まかなイメージとしてResponderで返答のバリエーションを作り、#
#UnmoでResponderを入れ、返答するAIをつくる#
#main.pyにはUnmo(Responder付)をいれ返答種類の表示#