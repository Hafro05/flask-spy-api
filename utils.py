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
    if ip == '127.0.0.1':
        ip = '8.8.8.8'
    try:
        url = f"https://ipwho.is/{ip}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(data)
            if data.get("success"):
                city = data.get("city")
                country = data.get("country")
                flag = data.get("flag").get("emoji")
                if city and country:
                    return f"{city}, {country} {flag}"
                elif country:
                    return country
    except Exception as e:
        print(f"[Erreur ipwho.is] {e}")
    return "Inconnu"

