from flask import Flask, jsonify, render_template
from scraper import get_victoria_events, summarize_event

app= Flask(__name__)

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/api/events")
def events():
    raw_events = get_victoria_events()

    summarized=[]
    for event in raw_events[:6]:
        event["summary"] = summarize_event(event)
        summarized.append(event)

    return jsonify(summarized)

if __name__ == "__main__":
    app.run(debug=True)