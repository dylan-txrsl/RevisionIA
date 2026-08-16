#Lecture de la configuration locale de DeepSeek

from dataclasses import dataclass
from pathlib import Path

DEFAULT_MODEL = "deepseek-v4-flash"
DEFAULT_BASE_URL = "https://api.deepseek.com"

@dataclass
#valeurs nécessaires pour appeler DeepSeek
class DeepSeekConfig:
    api_key: str
    model: str = DEFAULT_MODEL
    base_url: str = DEFAULT_BASE_URL

#charge la configuration DeepSeek depuis le fichier .env
def load_config():
    env_path = Path(__file__).resolve().parent / ".env"
    values = {}

    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines() #read_text() lit le fichier entier en une seule chaîne de caractères, puis splitlines() divise cette chaîne en une liste de lignes

        for line in lines:
            line = line.strip()

            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip() #strip pour enelever les espaces autour du nom et de la valeur

    return DeepSeekConfig(
        api_key=values.get("DEEPSEEK_API_KEY", ""),
        model=values.get("DEEPSEEK_MODEL", DEFAULT_MODEL),
        base_url=values.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL),
    )
