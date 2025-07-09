import requests
from flask import request
from user_agents import parse

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
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data.get('city', 'Ville inconnue')
        else:
            return "Ville inconnue"
    except Exception:
        return "Ville inconnue"
