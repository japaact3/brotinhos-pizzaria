self.addEventListener("install", e => {
    console.log("Service Worker instalado");
});

self.addEventListener("fetch", e => {
    // versão simples: só deixa passar
});