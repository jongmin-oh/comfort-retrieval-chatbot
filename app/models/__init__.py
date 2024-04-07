class KakaoTemplate:
    def __init__(self):
        # 탬플릿 버전
        self.version = "2.0"

    # 텍스트 출력요소
    def text_component(self, text):
        return {"simpleText": {"text": text}}

    def send_response(self, utterance):
        response_body = {"version": self.version, "template": {"outputs": []}}

        if utterance is not None:
            response_body["template"]["outputs"].append(self.text_component(utterance))
        return response_body


skillTemplate = KakaoTemplate()
