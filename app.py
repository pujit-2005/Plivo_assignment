import os
from flask import Flask, request, make_response
import plivo
from plivo import plivoxml

app = Flask(__name__)

AUTH_ID = "MAMTAWMGIOMZCTNTYZZS"
AUTH_TOKEN = "M2Y2MzIIMWEtOGU5Ny00YzYxLWFkNzItZmE5ZmNI"
PLIVO_NUMBER = "+918035454161"
ASSOCIATE_NUMBER = "02264236412"
MY_NUMBER = "+919311398730" 
HARDCODED_OTP = "2204" 
BASE_URL = "https://reverse-sliding-reissue.ngrok-free.dev"
client = plivo.RestClient(AUTH_ID, AUTH_TOKEN)

@app.route('/make_call', methods=['GET', 'POST'])
def make_call():
    try:
        response = client.calls.create(
            from_=PLIVO_NUMBER,
            to_=MY_NUMBER,
            answer_url=f"{BASE_URL}/answer",
            answer_method='POST'
        )
        return {"status": "success", "message": "Call initiated", "api_id": response.api_id}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/answer', methods=['POST'])
def answer_call():
    response = plivoxml.ResponseElement()
    get_input = response.add(
        plivoxml.GetInputElement(
            action=f"{BASE_URL}/process_otp",
            method='POST',
            input_type='dtmf',
            digit_end_timeout=5,
            num_digits=4
        )
    )
    get_input.add(
        plivoxml.SpeakElement("Welcome to InspireWorks. Please enter your 4 digit O T P.")
    )
    return make_response(response.to_string(), 200, {'Content-Type': 'application/xml'})

@app.route('/process_otp', methods=['POST'])
def process_otp():
    digits = request.form.get('Digits')
    response = plivoxml.ResponseElement()

    if digits == HARDCODED_OTP:
        get_input = response.add(
            plivoxml.GetInputElement(
                action=f"{BASE_URL}/ivr_level_1",
                method='POST',
                input_type='dtmf',
                num_digits=1
            )
        )
        get_input.add(
            plivoxml.SpeakElement("Authentication successful. For English, press 1. For Spanish, press 2.")
        )
    else:
        get_input = response.add(
            plivoxml.GetInputElement(
                action=f"{BASE_URL}/process_otp",
                method='POST',
                input_type='dtmf',
                num_digits=4
            )
        )
        get_input.add(
            plivoxml.SpeakElement("Incorrect O T P. Please try again.")
        )
    
    return make_response(response.to_string(), 200, {'Content-Type': 'application/xml'})

@app.route('/ivr_level_1', methods=['POST'])
def ivr_level_1():
    digits = request.form.get('Digits')
    response = plivoxml.ResponseElement()

    if digits in ['1', '2']:
        language = "English" if digits == '1' else "Spanish"
        get_input = response.add(
            plivoxml.GetInputElement(
                action=f"{BASE_URL}/ivr_level_2?lang={language}",
                method='POST',
                input_type='dtmf',
                num_digits=1
            )
        )
        msg = "Press 1 to play a short audio message. Press 2 to connect to a live associate."
        if language == "Spanish":
            msg = "Presione 1 para reproducir un mensaje de audio. Presione 2 para conectarse con un asociado."
            
        get_input.add(plivoxml.SpeakElement(msg))
    else:
        get_input = response.add(
            plivoxml.GetInputElement(
                action=f"{BASE_URL}/ivr_level_1",
                method='POST',
                input_type='dtmf',
                num_digits=1
            )
        )
        get_input.add(plivoxml.SpeakElement("Invalid input. For English, press 1. For Spanish, press 2."))

    return make_response(response.to_string(), 200, {'Content-Type': 'application/xml'})

@app.route('/ivr_level_2', methods=['POST'])
def ivr_level_2():
    digits = request.form.get('Digits')
    language = request.args.get('lang', 'English')
    response = plivoxml.ResponseElement()

    if digits == '1':
        response.add(
            plivoxml.PlayElement("https://s3.amazonaws.com/plivocloud/music.mp3")
        )
    elif digits == '2':
        response.add(
            plivoxml.SpeakElement("Connecting you to a live associate now." if language == "English" else "Conectando con un asociado ahora.")
        )
        response.add(
            plivoxml.DialElement().add(
                plivoxml.NumberElement(ASSOCIATE_NUMBER)
            )
        )
    else:
        get_input = response.add(
            plivoxml.GetInputElement(
                action=f"{BASE_URL}/ivr_level_2?lang={language}",
                method='POST',
                input_type='dtmf',
                num_digits=1
            )
        )
        msg = "Invalid input. Press 1 for audio, or 2 for an associate."
        get_input.add(plivoxml.SpeakElement(msg))

    return make_response(response.to_string(), 200, {'Content-Type': 'application/xml'})

if __name__ == '__main__':
    app.run(port=5000)