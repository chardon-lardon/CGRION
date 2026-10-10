"""Coordonne la réponse et la mémoire."""
from ai import generate_response
from memory import remember


def respond(message):
    response = generate_response(message)
    remember(message, response)
    return response
