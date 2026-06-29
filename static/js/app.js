function emBreve() {
    mostrarToast("funcionalidade Disponível Em Breve!", 'success');
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js');
}