document.getElementById("anemiaForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const data = {
        gender: parseInt(document.getElementById("gender").value),
        hemoglobin: parseFloat(document.getElementById("hemoglobin").value),
        mch: parseFloat(document.getElementById("mch").value),
        mchc: parseFloat(document.getElementById("mchc").value),
        mcv: parseFloat(document.getElementById("mcv").value)
    };

    const resultElement = document.getElementById("result");

    resultElement.innerText = "Processing prediction...";

    try {
        const response = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Prediction request failed");
        }

        resultElement.textContent = result.result;

    } catch (error) {
        console.error("Prediction error:", error);

        resultElement.textContent =
            "Unable to get prediction. Please try again.";
    }
});

function resetForm() {
    document.getElementById("anemiaForm").reset();
    document.getElementById("result").innerText = "";
}
