let currentData = null;
let imagePath = null;

async function extractData() {

    const file =
        document.getElementById("file").files[0];

    if (!file) {
        alert("Choisissez une image.");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        const response = await fetch("/extract", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        currentData = result.data;
        imagePath = result.image_path;

        document
            .getElementById("preview-image")
            .src = URL.createObjectURL(file);

        showForm();

    } catch (error) {

        console.error(error);

        alert("Erreur lors de l'analyse.");

    }
}

function showForm() {

    const editor =
        document.getElementById("editor");

    const form =
        document.getElementById("form");

    let html = "";

    for (const key in currentData) {

        html += `
            <div class="field">
                <label>${key}</label>

                <input
                    id="${key}"
                    value="${currentData[key] ?? ""}">
            </div>
        `;
    }

    html += `
        <button
            class="save-btn"
            onclick="saveData()">
            Enregistrer
        </button>
    `;

    form.innerHTML = html;

    editor.classList.remove("hidden");
}

async function saveData() {

    for (const key in currentData) {

        const input =
            document.getElementById(key);

        currentData[key] =
            input.value;
    }

    try {

        const response = await fetch(
            "/save",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    image_path: imagePath,
                    data: currentData
                })
            }
        );

        const result =
            await response.json();

        if (result.success) {

            alert(
                "Note de frais enregistrée."
            );

        } else {

            alert(
                "Erreur d'enregistrement."
            );

        }

    } catch (error) {

        console.error(error);

        alert(
            "Erreur serveur."
        );

    }
}