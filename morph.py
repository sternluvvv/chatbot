import re #正規表現#
from janome.tokenizer import Tokenizer

TOKENIZER = Tokenizer()




def analyze(text) :
    return [(t.surface, t.part_of_speech) for t in TOKENIZER.tokenize(text)]
                        #textを形態素解析して1行ごとに読み、(surface,parts)のかたちにして改行されていく surface(品詞) part(形態素解析の結果)#
    
def is_keyword(part) :
    return bool(re.match(r'名詞,(一般|代名詞|固有名詞|サ変接続|形容動詞語幹)',part)) #boolは真偽値。partと名詞の部類がマッチすればtrueを返す。他の品詞の場合だめ#
