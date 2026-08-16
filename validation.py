#règles de validation du texte

MINIMUM_CHARACTERS = 50
MAXIMUM_CHARACTERS = 12_000

#pour centraliser l'erreur de validation du texte de cours
class TextValidationError(ValueError):
    pass

#valide le texte de cours et renvoie le texte
def validate_course_text(text):
    """Nettoie le texte et vérifie qu'il peut être envoyé à DeepSeek."""

    cleaned_text = text.strip()

    if not cleaned_text:
        raise TextValidationError("Colle d'abord un texte de cours.")

    if len(cleaned_text) < MINIMUM_CHARACTERS:
        raise TextValidationError(
            f"Le texte doit contenir au moins {MINIMUM_CHARACTERS} caractères."
        )

    if len(cleaned_text) > MAXIMUM_CHARACTERS:
        raise TextValidationError(
            f"Le texte ne doit pas dépasser {MAXIMUM_CHARACTERS} caractères."
        )

    return cleaned_text

#on compte juste les mots séparés par des espaces.
def count_words(text):
    return len(text.split())
