/* MODAL DE SELEÇÃO DE SABORES*/

function abrirModal() {
    document.getElementById("modal").style.display = "flex";
}

function fecharModal() {
    document.getElementById("modal").style.display = "none";
}


function alterarQtd(id, valor) {

    if (!itens[id]) {
        itens[id] = 0;
    }

    itens[id] += valor;

    if (itens[id] < 0) {
        itens[id] = 0;
    }

    document.getElementById(`qtd-${id}`).innerText = itens[id];
}