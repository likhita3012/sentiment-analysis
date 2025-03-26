from flask import Flask, render_template, request, jsonify
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download NLTK resources
nltk.download('vader_lexicon')

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Flask app
app = Flask(__name__)

# Predefined chatbot responses
responses = {
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm just a bot, but I'm doing great!",
    "bye": "Goodbye! Have a nice day.",
    "default": "I'm not sure how to respond to that. Can you rephrase?"
}

# Function to analyze sentiment
def analyze_sentiment(text):
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return "Positive 😊"
    elif score['compound'] <= -0.05:
        return "Negative 😞"
    else:
        return "Neutral 😐"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"].lower()
    bot_response = responses.get(user_message, responses["default"])
    sentiment = analyze_sentiment(user_message)
    
    return jsonify({"bot_response": bot_response, "sentiment": sentiment})

if __name__ == "__main__":
    app.run(debug=True)
