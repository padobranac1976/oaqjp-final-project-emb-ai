"""This module deploys the funcionality of the emotion detection 
to a local host and handles errors for empty input string
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector, format_final_statement

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotion_analyzer():
    """Runs the emotion detection algorithm and handles empty re
    """
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        final_statement = " Invalid text! Please try again!"
    else:
        final_statement = format_final_statement(response)
    return final_statement

@app.route("/")
def render_index_page():
    """Render index page
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
