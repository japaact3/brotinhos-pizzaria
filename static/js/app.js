function emBreve() {
    mostrarToast("funcionalidade Disponível Em Breve!", 'success');
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js');
}

function abrirModalReset() {
    document.getElementById("modalReset").style.display = "flex";
}

function fecharModalReset() {
    document.getElementById("modalReset").style.display = "none";
}

function confirmarReset() {
    fetch("/reset-semana", {
        method: "POST"
    })
    .then(res => res.json())
    .then(() => {
        mostrarToast("Historico Resetado!", 'success');
        fecharModalReset();
        
        location.reload();
    });
}