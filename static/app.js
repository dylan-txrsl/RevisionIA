// Récupère les éléments de la page
const form = document.querySelector("#revision-form");
const courseText = document.querySelector("#course-text");
const textCounter = document.querySelector("#text-counter");
const generateButton = document.querySelector("#generate-button");
const clearButton = document.querySelector("#clear-button");
const statusBadge = document.querySelector("#status-badge");
const emptyResult = document.querySelector("#empty-result");
const errorMessage = document.querySelector("#error-message");
const resultContent = document.querySelector("#result-content");
const downloadButton = document.querySelector("#download-button");

let resultText = "";


// Met à jour le compteur
courseText.addEventListener("input", function () {
    textCounter.textContent = courseText.value.length + " / 12 000";
});


// Envoie le cours à Python
form.addEventListener("submit", async function (event) {
    event.preventDefault();

    generateButton.disabled = true;
    generateButton.textContent = "Création en cours...";
    statusBadge.textContent = "Analyse...";

try {
    // Envoie le texte du cours à la route FastAPI
    const response = await fetch("/api/generate", {
        method: "POST",

        // Indique que les données sont au format JSON
        headers: {"Content-Type": "application/json"},

        // Transforme le texte du cours en JSON
        body: JSON.stringify({
            course_text: courseText.value
        })
    });

    // Transforme la réponse JSON en objet JavaScript
    const data = await response.json();

    // Déclenche une erreur si FastAPI signale un problème
    if (!response.ok) {
        throw new Error(data.detail);
    }

        resultText = data.result;
        resultContent.textContent = resultText;
        resultContent.hidden = false;
        emptyResult.hidden = true;
        errorMessage.hidden = true;
        downloadButton.hidden = false;
        statusBadge.textContent = "Fiche terminée";

    } catch (error) {
        errorMessage.textContent = error.message;
        errorMessage.hidden = false;
        resultContent.hidden = true;
        downloadButton.hidden = true;
        statusBadge.textContent = "Erreur";
    }

    generateButton.disabled = false;
    generateButton.textContent = "Transformer ce texte en fiche";
});


// Efface le texte et le résultat
clearButton.addEventListener("click", function () {
    courseText.value = "";
    resultText = "";
    resultContent.textContent = "";
    resultContent.hidden = true;
    errorMessage.hidden = true;
    downloadButton.hidden = true;
    emptyResult.hidden = false;
    statusBadge.textContent = "En attente";
    textCounter.textContent = "0 / 12 000";
});


// Télécharge la fiche
downloadButton.addEventListener("click", function () {
    const file = new Blob([resultText], {type: "text/plain"});
    const link = document.createElement("a");

    link.href = URL.createObjectURL(file);
    link.download = "fiche_revision.txt";
    link.click();
});
