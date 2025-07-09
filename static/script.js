async function callApi() {
    const prenom = document.getElementById('prenomInput').value.trim();
    const responseBox = document.getElementById('responseBox');
    const loader = document.getElementById('loader');
  
    if (!prenom) {
      responseBox.textContent = "⛔ Merci d'entrer un prénom.";
      return;
    }
  
    loader.classList.add('show');
    responseBox.textContent = "";
  
    try {
      const res = await fetch('/whoami', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prenom })
      });
  
      const data = await res.json();
      loader.classList.remove('show');
  
      if (res.ok) {
        responseBox.textContent = `
  👤 ${data.message}
  🌍 Ville : ${data.ville}
  💻 OS : ${data.os}
  🌐 Navigateur : ${data.browser}
  🔮 Prédiction : ${data.prediction}
  📅 Timestamp : ${data.timestamp}
        `.trim();
      } else {
        responseBox.textContent = `⚠️ Erreur : ${data.error || "Erreur inconnue."}`;
      }
    } catch (err) {
      loader.classList.remove('show');
      responseBox.textContent = "💥 Erreur réseau : " + err.message;
    }
  }
  