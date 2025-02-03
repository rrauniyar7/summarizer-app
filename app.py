from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Read the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Configure OpenAI API
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

def summarize_article(article_text):
    """
    Summarizes the provided article text using OpenAI's GPT-3.5-turbo model.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Faster model
            messages=[
                {"role": "system", "content": "You are an AI assistant specialized in summarizing text."},
                {"role": "user", "content": f"Summarize this article: {article_text}"}
            ],
            max_tokens=100,  # Shorter summary
            temperature=0.3  # More deterministic output
        )
        summary = response.choices[0].message['content']
        return summary.strip()
    except Exception as e:
        return f"Error occurred: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    """
    Endpoint to handle summarization requests.
    """
    data = request.get_json()
    article_text = data.get("text", "")
    summary = summarize_article(article_text)  # Directly call the function
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)