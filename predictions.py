import random

def get_random_prediction():
    phrases = [
        "Tu vas corriger un bug sans comprendre pourquoi.",
        "Un commit te trahira bientôt.",
        "Ton café va refroidir avant le push final.",
        "Tu vas briller en réunion sans avoir bossé.",
        "Un merge conflict t’attend dans l’ombre."
    ]
    return random.choice(phrases)
