import os
from flask import Flask, request, jsonify, send_from_directory
from models import db, UserInfo
from predictions import get_random_prediction
from utils import get_ip, parse_user_agent, get_city_from_ip
from flasgger import Swagger, swag_from

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
Swagger(app)
db.init_app(app)
with app.app_context():
    if not os.path.exists("data.db"):
        print("👉 Création de la base de données...")
        db.create_all()

@app.route('/whoami', methods=['POST'])
def whoami():
    """
    Enregistre ou récupère un utilisateur via son IP

    ---
    tags:
      - Utilisateur
    parameters:
      - name: prenom
        in: body
        required: true
        schema:
          type: object
          properties:
            prenom:
              type: string
              example: Alice
    responses:
      200:
        description: Utilisateur déjà existant
        schema:
          id: User
          properties:
            message:
              type: string
            ip:
              type: string
            ville:
              type: string
            prediction:
              type: string
      201:
        description: Nouvel utilisateur enregistré
    """
    data = request.get_json()
    prenom = data.get('prenom')

    if not prenom:
        return jsonify({"error": "Le champ 'prenom' est obligatoire."}), 400

    ip = get_ip()
    existing = UserInfo.query.filter_by(prenom=prenom,ip=ip).first()
    if existing:
        return jsonify({
            "message": f"Rebienvenue {existing.prenom}, tu es déjà fiché 🕵️",
            "ip": existing.ip,
            "ville": existing.ville,
            "os": existing.os,
            "browser": existing.browser,
            "prediction": existing.prediction,
            "timestamp": existing.created_at.isoformat()
        }), 200
    
    # Sinon, nouvelle entrée
    user_agent_str = request.headers.get('User-Agent', '')
    ua_info = parse_user_agent(user_agent_str)
    ville = get_city_from_ip(ip)
    prediction = get_random_prediction()

    user = UserInfo(
        prenom=prenom,
        ip=ip,
        os=ua_info['os'],
        browser=ua_info['browser'],
        user_agent=user_agent_str,
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
    }), 201


@app.route("/reset", methods=["POST"])
@swag_from({
    'tags': ['Admin'],
    'summary': "Réinitialise la base de données",
    'description': "⚠️ Supprime toutes les données et recrée les tables.",
    'responses': {
        200: {
            'description': "Base de données réinitialisée avec succès.",
            'examples': {
                'application/json': {
                    'message': 'Base de données réinitialisée.'
                }
            }
        }
    }
})
def reset_db():
    db.drop_all()
    db.create_all()
    return jsonify({"message": "Base de données réinitialisée."}), 200

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
