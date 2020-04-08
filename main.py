class Responder :
    
    def __init__(self,name) :
        self._name = name #Responderの名前(変更不可）#

    def response(self,text) :
        return '{}って何？'.format(text)

    @property           #respondername.nameでできる
    def name(self):
        return self._name

class Unmo:
    def __init__(self,name) :
        self._name = name
        self._responder = Responder('What') #UnmoにはWhatと言う名前のresponderクラスの要素がある#

    def dialoue(self,text) :
        return self._responder.response(text) #Whatのresponseをもってきた#

    @property
    def name(self) :
        return self._name

    @property
    def responder_name(self):
        return self._responder.name #Whatとでるはず#

def build_prompt(unmo) :        #selfでもいいけどわかりやすくunmo#
        return '{name}:{responder}>'.format(name=unmo.name,responder=unmo.responder_name)
                                    #name=self.name(unmoの名前)　self.responder_name(Whatとでる)#
if __name__ == '__main__' :      #import main としたとき勝手に動かないようにするため.Trueが返される#
        print('Unmo System prototype : proto') 
        proto = Unmo('proto')
        while True :            
            text = input('>')
            if not text :
                break

            response = proto.dialoge(text) #proto(Unmo)のdialoge(What(Responder)のresponse)｛って何？｝#
            print('{prompt}{response}'.format(prompt=build_prompt(prot),response = response))   #prot:What> って何？#となる