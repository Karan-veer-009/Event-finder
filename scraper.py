import requests
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")

def get_victoria_events():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    
    params = {
        "apikey": TICKETMASTER_API_KEY,
        "city": "Victoria",
        "countryCode": "CA",
        "size": 20
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    events = []
    
    for event in data.get("_embedded", {}).get("events", []):
        events.append({
            "title": event["name"],
            "date": event["dates"]["start"]["localDate"],
            "url": event["url"],
            "description": event.get("info", "No description available")
        })
    
    return events

def summarize_event(event):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": f"Summarize this event in exactly 2 short sentences for a university student. Make it sound fun and relevant. Event: {event['title']} on {event['date']}. Details: {event['description']}"}]
    )
    
    return response.content[0].text
if __name__ == "__main__":
    events = get_victoria_events()
    print(f"Found {len(events)} events")

    for e in events[:3]:
        print("Event:", e["title"])
        print("Date:", e["date"])
        summary = summarize_event(e)
        print("AI Summary:", summary)
        print("---")