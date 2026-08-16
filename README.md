# RévisionIA

RévisionIA transforme un texte de cours en fiche de révision avec DeepSeek.
Le programme produit un résumé, les notions importantes, cinq questions et
leurs réponses.

## Fonctionnalités

- interface web HTML/CSS simple et responsive ;
- bouton explicite pour lancer la transformation ;
- contrôle de la longueur du texte ;
- compteur de caractères ;
- génération avec l'API DeepSeek ;
- affichage des erreurs dans la page ;
- téléchargement de la fiche en `.txt`.

## Technologies

- Python 3.10 ou plus récent ;
- FastAPI pour le serveur et la route Python ;
- HTML et CSS pour l'interface ;
- JavaScript pour relier le bouton au serveur ;
- `urllib` et `json` pour contacter DeepSeek ;
- Git et GitHub pour suivre l'évolution.

## Structure

```text
RevisionIA/
├── main.py                 # serveur FastAPI et routes
├── validation.py           # règles appliquées au texte
├── config.py               # lecture du fichier .env
├── deepseek_service.py     # communication avec DeepSeek
├── templates/
│   └── index.html          # structure de la page
├── static/
│   ├── styles.css          # apparence de la page
│   └── app.js              # clic du bouton et affichage du résultat
├── .env.example            # exemple de configuration
├── .gitignore              # fichiers exclus de Git
└── requirements.txt        # bibliothèques à installer
```

## Installation

Depuis PowerShell, dans le dossier du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copier `.env.example` sous le nom `.env`, puis ajouter la clé DeepSeek :

```env
DEEPSEEK_API_KEY=ta_cle_deepseek
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## Démarrage

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Ouvrir ensuite <http://127.0.0.1:8000/>.

## Utilisation

1. Coller un texte d'au moins 50 caractères.
2. Cliquer sur **Transformer ce texte en fiche**.
3. Attendre la réponse de DeepSeek.
4. Lire ou télécharger la fiche générée.

Une connexion Internet et des crédits DeepSeek sont nécessaires. La clé `.env`
reste locale et n'est jamais ajoutée à Git.