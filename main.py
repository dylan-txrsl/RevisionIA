#Serveur principal de l'application RévisionIA

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from deepseek_service import DeepSeekError, create_revision_sheet
from validation import TextValidationError, count_words, validate_course_text


project_folder = Path(__file__).parent

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=project_folder / "static"),
)

#définit la forme du texte reçu depuis JavaScript
class GenerationRequest(BaseModel):
    course_text: str


#affiche la page HTML principale
@app.get("/")
def show_home_page():
    return FileResponse(project_folder / "templates" / "index.html")


#reçoit le cours, le valide, appelle DeepSeek et retourne la fiche
@app.post("/api/generate")
def generate_revision_sheet(request: GenerationRequest):

    try:
        course_text = validate_course_text(request.course_text)
    except TextValidationError as error:
        raise HTTPException(status_code=400, detail=str(error))

    try:
        result = create_revision_sheet(course_text)
    except DeepSeekError as error:
        raise HTTPException(status_code=502, detail=str(error))

    return {
        "result": result,
        "word_count": count_words(course_text),
    }