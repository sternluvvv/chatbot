from unmo import Unmo  # unmo.pyからUnmoと言う名前をロード(if nameでunmoを使ってる為#

def build_prompt(unmo) :        #selfでもいいけどわかりやすくunmo#
    return '{name}:{responder}>'.format(name=unmo.name,responder=unmo.responder_name)

if __name__ == '__main__' :      #import main としたとき勝手に動かないようにするため.Trueが返される#
    print('Unmo System prototype : proto') 
    proto = Unmo('proto')
    while True :            
        text = input('>')
        if not text :
            break
        try :
            response = proto.dialogue(text) #proto(Unmo)のdialoge(What(Responder)のresponse)｛って何？｝#
        except IndexError as error :
            print('{}:{}'.format(type(error).__name__, str(error)))
            print('警告：辞書が空です。(Responder:{})'.format(proto.responder_name))
        else :
            print('{prompt}{response}'.format(prompt=build_prompt(proto),response = response))   #prot:What> って何？#となる#
    
    proto.save()