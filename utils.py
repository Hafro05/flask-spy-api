import requests
from flask import request

def get_ip():
    # X-Forwarded-For = si derrière un proxy (Heroku, nginx...)
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def parse_user_agent():
    ua = request.user_agent
    return {
        "os": ua.platform or "Inconnu",
        "browser": ua.browser or "Inconnu",
        "user_agent": str(ua)
    }

def get_city_from_ip(ip):
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data.get('city', 'Ville inconnue')
        else:
            return "Ville inconnue"
    except Exception:
        return "Ville inconnue"
