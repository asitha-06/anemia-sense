const form = document.getElementById("anemiaForm");
const resultBox = document.getElementById("result");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = {
        gender: Number(document.getElementById("gender").value),
        hemoglobin: Number(
            document.getElementById("hemoglobin").value
        ),
        mch: Number(document.getElementById("mch").value),
        mchc: Number(document.getElementById("mchc").value),
        mcv: Number(document.getElementById("mcv").value)
    };

    resultBox.textContent = "Processing prediction...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const responseText = await response.text();

        let result;

        try {
            result = JSON.parse(responseText);
        } catch {
            throw new Error(
                `The server returned an unexpected response (HTTP ${response.status}).`
            );
        }

        if (!response.ok) {
            throw new Error(
                result.error || `Request failed: HTTP ${response.status}`
            );
        }

        if (!result.result) {
            throw new Error("The server did not return a prediction.");
        }

        const message = document.createElement("p");
        message.textContent = result.result;

        resultBox.replaceChildren(message);

    } catch (error) {
        console.error("Prediction error:", error);

        const message = document.createElement("p");
        message.textContent = error.message;

        resultBox.replaceChildren(message);
    }
});


function resetForm() {
    form.reset();
    resultBox.textContent = "";
}
