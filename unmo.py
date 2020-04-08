from responder import RandomResponder #responder.pyからResponderと言う名前のロード(Responder('What')#

class Unmo:
    def __init__(self,name) :
        self._name = name
        self._responder = RandomResponder('Random') #UnmoにはWhatと言う名前のresponderクラスの要素がある#

    def dialogue(self,text) :
        return self._responder.response(text) #RandomResponderのresponseをもってきた#

    @property
    def name(self) :
        return self._name

    @property
    def responder_name(self):
        return self._responder.name #Randomとでるはず#

