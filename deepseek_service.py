#Communication avec l'API DeepSeek

import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import load_config


SYSTEM_PROMPT = """Tu es un assistant pédagogique francophone.
Transforme le texte fourni en une fiche de révision fidèle au contenu.
Utilise exactement cette structure :

TITRE
Un titre court

RÉSUMÉ
Un résumé clair de cinq phrases maximum

NOTIONS CLÉS
- Une liste des notions importantes

QUESTIONS DE RÉVISION
1. Cinq questions permettant de vérifier la compréhension

RÉPONSES
1. Les réponses courtes correspondant aux cinq questions

N'invente aucune information absente du texte."""


class DeepSeekError(Exception):
    """Erreur lors de la communication avec DeepSeek."""


def create_revision_sheet(course_text):
    config = load_config()

    if config.api_key == "" or config.api_key == "colle_ta_cle_ici":
        raise DeepSeekError("La clé DeepSeek manque dans le fichier .env.")

#recup le modèle dans load_config() et construit le corps de la requête à envoyer à DeepSeek
    body = build_request_body(course_text, config.model)

#informations d'authentification et type de contenu pour l'API DeepSeek
    headers = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }

#prépare la requête HTTP à envoyer à DeepSeek
    request = Request(
        url=config.base_url + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            response_text = response.read().decode("utf-8")
            response_data = json.loads(response_text)

    except HTTPError as error:
        raise DeepSeekError(http_error_message(error.code))

    except URLError:
        raise DeepSeekError(
            "Impossible de contacter DeepSeek. Vérifie ta connexion Internet."
        )

    except json.JSONDecodeError:
        raise DeepSeekError("DeepSeek a renvoyé une réponse illisible.")

    return extract_generated_text(response_data)


#prépare les informations envoyées à DeepSeek
def build_request_body(course_text, model):
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": course_text},
        ],
        "thinking": {"type": "disabled"},
        "max_tokens": 1200,
        "stream": False,
    }

#récupère le texte généré dans la réponse de DeepSeek
def extract_generated_text(response_data):
    try:
        text = response_data["choices"][0]["message"]["content"].strip()

    except (KeyError, IndexError, TypeError, AttributeError):
        raise DeepSeekError("La réponse DeepSeek ne contient aucune fiche.")

    if text == "":
        raise DeepSeekError("DeepSeek a renvoyé une fiche vide.")

    return text

#transforme un code HTTP en message simple pour l'utilisateur
def http_error_message(status_code: int) -> str:

    if status_code == 401:
        return "La clé DeepSeek est incorrecte ou désactivée."
    if status_code == 402:
        return "Le compte DeepSeek ne possède plus assez de crédits."
    if status_code == 429:
        return "DeepSeek reçoit trop de demandes. Réessaie dans un instant."
    return f"DeepSeek a refusé la demande (erreur {status_code})."
