from flask import Flask , request , jsonify
from chatbot import chatbot_answer
from kakao_api import KakaoTemplate

skillTemplate = KakaoTemplate()

app = Flask(__name__)

@app.route("/chatbot", methods=['POST'])
def combotAPI():
    try:
        receive_data = request.get_json()
        query = str(receive_data['userRequest']['utterance'])
        
        app.logger.info(f"input query : {str(query)}")
        result = chatbot_answer(query)
        
        return jsonify(skillTemplate.send_response(result))
    except Exception as e:
        result = f"에러 : {e}"
        app.logger.info(f"error : {e}")
        return jsonify(skillTemplate.send_response(result))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000,threaded=True,debug=True)