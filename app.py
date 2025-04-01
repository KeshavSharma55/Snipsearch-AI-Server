from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace this with your actual API key
API_KEY = "AIzaSyAmBw0mW9P-OIPoODTyDcT5M-MAE124q9Q"

def get_gemini_response(query):
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": query}]}]
    }

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except KeyError:
            return "Sorry, I couldn't find an answer."
    else:
        return f"Error: {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["query"]
        response = get_gemini_response(user_input)
    return render_template("index.html", response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)