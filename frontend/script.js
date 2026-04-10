document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("sentimentForm");
    const reviewText = document.getElementById("reviewText");
    const submitBtn = document.getElementById("submitBtn");
    const btnText = document.querySelector(".btn-text");
    const spinner = document.getElementById("spinner");
    
    const resultContainer = document.getElementById("resultContainer");
    const sentimentResult = document.getElementById("sentimentResult");
    const confidenceBar = document.getElementById("confidenceBar");
    const confidenceValue = document.getElementById("confidenceValue");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const review = reviewText.value.trim();
        if (!review) return;

        // UI Loading State
        submitBtn.disabled = true;
        btnText.textContent = "Analyzing Review...";
        spinner.style.display = "block";
        
        // Hide previous result
        resultContainer.classList.add("hidden");
        // Reset progress bar to animate again later
        confidenceBar.style.width = "0%";

        try {
            // Adjust the URL if your FastAPI backend runs on a different host/port
            const response = await fetch("http://localhost:8000/api/review", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ review_text: review })
            });

            if (!response.ok) {
                throw new Error("Failed to connect to the server");
            }

            const data = await response.json();
            
            // Render Result nicely after a tiny manual delay to make the UI feel thoughtful
            setTimeout(() => {
                renderResult(data.sentiment, data.confidence);
            }, 300);

        } catch (error) {
            console.error("API Fetch Error:", error);
            alert("Could not reach backend server. Please verify the FastAPI backend is running on http://localhost:8000");
        } finally {
            // Restore UI State
            submitBtn.disabled = false;
            btnText.textContent = "Analyze Sentiment";
            spinner.style.display = "none";
        }
    });

    function renderResult(sentiment, confidence) {
        
        // Convert confidence to percentage
        const confPercent = Math.round(confidence * 100);
        confidenceValue.textContent = confPercent;

        // Reset text classes
        sentimentResult.className = "";

        if (sentiment === "Positive") {
            sentimentResult.textContent = "Positive";
            sentimentResult.classList.add("sentiment-positive");
            confidenceBar.style.background = "linear-gradient(90deg, #2ea043, #3fb950)";
        } else if (sentiment === "Negative") {
            sentimentResult.textContent = "Negative";
            sentimentResult.classList.add("sentiment-negative");
            confidenceBar.style.background = "linear-gradient(90deg, #da3633, #f85149)";
        } else {
            sentimentResult.textContent = "Neutral";
            sentimentResult.classList.add("sentiment-neutral");
            confidenceBar.style.background = "linear-gradient(90deg, #6e7681, #8b949e)";
        }

        // Display the container
        resultContainer.classList.remove("hidden");

        // Animate the confidence bar slightly after the container appears
        setTimeout(() => {
            confidenceBar.style.width = `${confPercent}%`;
        }, 50);
    }
});
