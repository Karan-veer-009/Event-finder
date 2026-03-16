import requests
import os
from dotenv import load_dotenv

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

if __name__ == "__main__":
    events = get_victoria_events()
    print(f"Found {len(events)} events")
    for e in events:
        print(e["title"], "-", e["date"])