document.getElementById("searchBtn").addEventListener("click", async () => {
  const journal = document.getElementById("journalInput").value.trim();
  const resultBox = document.getElementById("result");
  resultBox.innerHTML = "查询中...";

  try {
    // const res = await fetch(`http://localhost:5050/rank?journal=${encodeURIComponent(journal)}`);
    const res = await fetch(`https://journal-ranking-extension.onrender.com/rank?journal=${encodeURIComponent(journal)}`)
    const data = await res.json();

    if (data.error) {
      resultBox.innerHTML = `❌ ${data.error}`;
    } else {
      resultBox.innerHTML = renderResult(data);
      localStorage.setItem("lastQuery", JSON.stringify(data));
    }
  } catch (e) {
    resultBox.innerHTML = "查询失败，请检查服务是否启动。";
  }
});

document.getElementById("clearBtn").addEventListener("click", () => {
  localStorage.removeItem("lastQuery");
  document.getElementById("result").innerHTML = "";
  document.getElementById("journalInput").value = "";
});

window.onload = function () {
  const lastQuery = localStorage.getItem("lastQuery");
  if (lastQuery) {
    const data = JSON.parse(lastQuery);
    document.getElementById("result").innerHTML = renderResult(data);
  }
};

function renderResult(data) {
  return `
    ✅ <b>${data.journal}</b><br>
    SJR：${data.sjr}<br>
    Quartile：${data.quartile}<br>
    H-Index：${data.hindex}<br>
    Publisher：${data.publisher}<br>
    Subject Area：${data.subject}<br>
    🔗 <a href="${data.sjr_link}" target="_blank">查看 SJR 页面</a>
  `;
}