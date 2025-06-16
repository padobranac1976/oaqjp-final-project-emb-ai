"""Function definitions to run the emotion detection API and formatting helpers
"""
import json
import requests

def emotion_detector(text_to_analyse):
    """Emotion detection API call including error handling for empty input
    """
    url = 'https://sn-watson-emotion.labs.skills.network/' + \
          'v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyse } }
    response = requests.post(url, json=input_json, headers=headers, timeout=100)
    if response.status_code == 400:
        no_text = {"anger": None,
                   "disgust": None,
                   "fear": None,
                   "joy": None,
                   "sadness": None,
                   "dominant_emotion": None}
        return no_text
    return format_response(response.text)

def format_response(response_to_format):
    """formatting response of the API call to return JSON 
    and add "dominant_emotion" key
    """
    dictionary = json.loads(response_to_format)
    formated_response = dictionary["emotionPredictions"][0]["emotion"]
    formated_response['dominant_emotion'] = max(formated_response, key=formated_response.get)
    return formated_response

def format_final_statement(response):
    """Formats response for the final display on index.html
    """
    dominant_emotion = response["dominant_emotion"]
    emotions = []
    for item in response:
        if item == "dominant_emotion":
            continue
        emotions.append(f"'{item}': {response[item]}")
    result_statement = ", ".join(emotions)

    last_comma_index = result_statement.rfind(',')
    result_statement = result_statement[:last_comma_index] + \
                       ' and' + result_statement[last_comma_index + 1:]

    final_statement = f"<p>For the given statement, the system response is {result_statement}. " \
                      + f"The dominant emotion is <b>{dominant_emotion}</b>.</p>"
    return final_statement
