import os
import requests
from flask import request
from user_agents import parse
from dotenv import load_dotenv

load_dotenv()
def get_ip():
    # X-Forwarded-For = si derrière un proxy (Heroku, nginx...)
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def parse_user_agent(user_agent_string):
    ua = parse(user_agent_string)
    return {
        "os": ua.os.family + " " + ua.os.version_string,            # Ex: 'iOS', 'Windows', 'Linux'
        "browser": ua.browser.family   # Ex: 'Chrome', 'Safari', 'Firefox'
    }

def get_city_from_ip(ip):
    try:
        access_key = os.getenv("IPAPI_KEY")
        url = f"http://api.ipapi.com/api/{ip}?access_key={access_key}&fields=city,country_name"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            city = data.get("city")
            country = data.get("country_name")
            if city and country:
                return f"{city}, {country}"
            elif country:
                return country
    except Exception as e:
        print(f"[Erreur IPAPI] {e}")
    return "Inconnu"


