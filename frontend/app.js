async function uploadFile() {
  const file = document.getElementById("fileinput").files[0];
  if (!file) return alert("Select a file first!");
  
  const fd = new FormData();
  fd.append("file", file);

  try {
    const res = await fetch("http://127.0.0.1:8000/upload_pdf", {
      method: "POST",
      body: fd,
    });
    const data = await res.json();
    document.getElementById("uploadRes").innerText = JSON.stringify(data, null, 2);

    if (data.file_id) {
      document.getElementById("fileIds").value = data.file_id;
    }
  } catch (err) {
    alert("Upload failed!");
    console.error(err);
  }
}

async function askQuery() {
  const query = document.getElementById("query").value.trim();
  const fileIds = document.getElementById("fileIds").value.trim();
  
  if (!query) return alert("Please enter a question!");

  const fd = new FormData();
  fd.append("query", query);
  if (fileIds) fd.append("file_ids", fileIds);

  try {
    const res = await fetch("http://127.0.0.1:8000/ask", {
      method: "POST",
      body: fd,
    });
    const data = await res.json();

    // Format result nicely
    let formatted = "";
    if (data.final_answer) {
      formatted += `🧠 Final Answer:\n${data.final_answer}\n\n`;
    }
    if (data.decision) {
      formatted += `🤖 Agents Used: ${data.decision.agents.join(", ")}\n`;
      formatted += `🧩 Decision Rationale: ${data.decision.rationale}\n`;
    }

    document.getElementById("resultArea").innerText = formatted || "No result returned.";
  } catch (err) {
    document.getElementById("resultArea").innerText = "Error processing your request.";
    console.error(err);
  }
}
