from flask import Flask, request, jsonify, send_from_directory
from models import db, UserInfo
from predictions import get_random_prediction
from utils import get_ip, parse_user_agent, get_city_from_ip

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db.init_app(app)

@app.route('/whoami', methods=['POST'])
def whoami():
    data = request.get_json()
    prenom = data.get('prenom')

    if not prenom:
        return jsonify({"error": "Le champ 'prenom' est obligatoire."}), 400

    ip = get_ip()
    ua_info = parse_user_agent()
    ville = get_city_from_ip(ip)
    prediction = get_random_prediction()

    user = UserInfo(
        prenom=prenom,
        ip=ip,
        os=ua_info['os'],
        browser=ua_info['browser'],
        user_agent=ua_info['user_agent'],
        ville=ville,
        prediction=prediction
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": f"Salut {prenom} !",
        "ip": ip,
        "ville": ville,
        "os": ua_info['os'],
        "browser": ua_info['browser'],
        "prediction": prediction,
        "timestamp": user.created_at.isoformat()
    })


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
