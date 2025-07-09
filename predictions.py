import random

phrases = [
        "Tu vas recevoir un message mystérieux aujourd’hui.",
        "Quelqu’un pense à toi en ce moment.",
        "Un bug va t’épargner sans que tu le saches.",
        "Tu vas croiser une IA plus sympa que moi.",
        "Tu vas changer de fond d’écran cette semaine.",
        "Quelqu’un va te poser une question inattendue.",
        "Un commit anodin va changer ton destin.",
        "Tu vas oublier ton mot de passe et retrouver ton âme.",
        "Demain, tu diras 'je le savais' sans raison.",
        "Ton café sera parfait, sauf s’il déborde.",
        "Une idée de projet va te réveiller cette nuit.",
        "Le code que tu n’as pas écrit va mieux marcher que celui que tu as écrit.",
        "Ton navigateur te cache quelque chose...",
        "Tu vas avoir une super idée dans les toilettes.",
        "Tu finiras ce projet. Vraiment. Peut-être.",
    ]

def get_random_prediction():
    return random.choice(phrases)
