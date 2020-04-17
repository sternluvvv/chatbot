import os
import sys
from random import choice
from collections import defaultdict
import re
import copy
import dill                     #dill[pythonのデータをファイルに保存したり、読み込む]#
import morph
import tqdm

class Markov :
    ENDMARK = '%END%'
    CHAIN_MAX = 30      #単語の最大数#

    def __init__(self) :
        self._dic = defaultdict(lambda: defaultdict(lambda: [])) #defaultdictはデフォルトのvalue値にリストオブジェクト(型)が入ったdict型の変数self._dict#
                                                        #lambda 引数:返値　
        self._starts = defaultdict(lambda: 0)   #単語の個数#

    def add_sentence(self,parts) :      #学習処理#
        if len(parts) < 3 : #3単語以上で構成された文章のみ学習#
            return
        parts = copy.copy(parts) #呼び出し元の値を変更しないようにcopyする#

        prefix1,prefix2 = parts.pop(0)[0],parts.pop(0)[0] #prefix1はpartsの初めの単語　prefix2は次#

        self.__add_start(prefix1)   #prefixが何回頭にきたか。(文頭に来る単語を測る)#

        for suffix , _ in parts :     #打った言葉を(surfase,part)の行で分け、中身を返す#
            self.__add_suffix(prefix1,prefix2,suffix)       #もし中身にデフォルトのsuffixがあれば追加#    
            prefix1, prefix2 = prefix2 , suffix     #言葉が終わるまで繰り返す#
        self.__add_suffix(prefix1, prefix2 ,Markov.ENDMARK) #最後はエンドでしめる#

    def __add_suffix(self, prefix1,prefix2, suffix) :   #(dicはデフォルトの)存在しないsuffixの追加#
        self._dic[prefix1][prefix2].append(suffix)

    def __add_start(self,prefix1):  #prefixが何回頭にきたか。(文頭に来る単語を測る)#
        self._starts[prefix1] += 1
        
    def generate(self,keyword) :    #生成処理#
        if not self._dic :      #辞書が空の場合はnoneを返す#
            return None

        prefix1 = keyword if self._dic[keyword] else choice(list(self._starts.keys()))
                                                #もしdelf._dicにkeywrd(prefix1)がなければ　starts(単語：単語の個数)のkeyからランダムに返す#
        prefix2 = choice(list(self._dic[prefix1].keys())) #prefix1：{prefix2：[fuffix],prefix2:[suffix]}のprefix1のvalueからえらぶ#

        words = [prefix1,prefix2]

        for _ in range(Markov.CHAIN_MAX) : #30回まわす#
            suffix = choice(self._dic[prefix1][prefix2]) 
            if suffix == Markov.ENDMARK :  
                break
            words.append(suffix)    #出てきたsuffixをwordsに保存#
            prefix1,prefix2 = prefix2, suffix       #変更しておく#

        return ''.join(words)

    def load(self,filename) : #辞書の保存と読み込み#
            with open(filename, 'rb') as f :    #txtではなくバイナリ(二進数)での読み#    
                self._dic, self._starts = dill.load(f)

    def save(self, filename) :
            with open(filename, 'wb') as f :
                dill.dump((self._dic,self._starts),f)   #dillは保存するときに使うpickleで無理ならdill#
                                                        #(self._dic,self._starts)をfに保存#
    

def main() :        #python markov.py boccha .txtと打つと以下が実行される#
    markov = Markov()
    sep = r'[。?？！!   ]+'     #エスケープシーケンスを展開せずそのままの値が出る# #+は連続を表わす#
    filename = sys.argv[1]      #コマンドラインの引数?# つまりbocchan.txtを読み込む#
    dicfile = '{}.dat'.format(filename)     #bocchan.txt.datを作る#
    if os.path.exists(dicfile) :    #もしdictfileが存在してたら#
        markov.load(dicfile)        #dictfileにself._dictとself._startsの保存と読み込み#

    else :                          #もしdicfile存在していなかったらdicfileの作成#
        with open(filename, encoding = 'utf-8') as f :  #bocchan.txtを開く#
            sentences = []
            for line in f :             #bocchan.txtを1行ずつ読み取る#
                sentences.extend(re.split(sep, line.strip())) #extend(list)でlistの中身を他のリストに追加。
                                                                #bocchan.txtのsepを消してsntencesに追加#
        for sentence in tqdm.tqdm(sentences) :
            if sentence :       #↓1行ごと解析していきself._dicに追加されていく#
                markov.add_sentence(morph.analyze(sentence))    #add_sentenceにはsurface,partに分れたものを渡すので、analyzeで処理しておく#
                #print('.',end = '')                             #改行なし#
                #sys.stdout.flush()                              #改行無しよりsentenceが横に追加されていく#
        markov.save(dicfile)    #全てをbocchan.txt.datに保存#
    print('\n')

    while True :
        line = input('>')
        if not line :
            break
        parts = morph.analyze(line)
        keyword = next((word for word,part in parts if morph.is_keyword(part)),'')
        print(markov.generate(keyword))
if __name__ == '__main__' :
    main()
                

