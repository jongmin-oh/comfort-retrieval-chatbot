class KakaoTemplate:
    def __init__(self):
        #탬플릿 버전
        self.version = "2.0"

    #텍스트 출력요소
    def TextComponent(self,text):
        return{
            "simpleText":{"text":text}
        }
    
    def send_response(self,utterance):
        responseBody = {
            "version":self.version,
            "template":{
                "outputs" : []
            }
        }

        if utterance is not None:
            responseBody['template']['outputs'].append(
                self.TextComponent(utterance)
            )
        return responseBody