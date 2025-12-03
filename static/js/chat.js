const form = document.getElementById("qa-form");
const questionInput = document.getElementById("question");
const answerSection = document.getElementById("answer");
const answerText = document.getElementById("answer-text");
const sourcesDiv = document.getElementById("sources");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = questionInput.value.trim();
  if (!question) return;

  form.querySelector("button").disabled = true;
  answerText.textContent = "Working on it...";
  sourcesDiv.textContent = "";
  answerSection.hidden = false;

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Request failed");
    }

    const data = await response.json();
    answerText.textContent = data.answer || "No answer returned.";
    if (data.sources?.length) {
      sourcesDiv.innerHTML = `<strong>Sources:</strong> ${data.sources
        .map((s) => `<span>${s}</span>`)
        .join(", ")}`;
    } else {
      sourcesDiv.textContent = "Sources: none";
    }
  } catch (error) {
    answerText.textContent = error.message;
  } finally {
    form.querySelector("button").disabled = false;
  }
});
