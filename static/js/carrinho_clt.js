/* =========================================================
   CARRINHO V2 - BROTHINHOS GALEGO
   COMPATÍVEL COM CLIENTE.CSS NOVO
========================================================= */

let carrinho = {};


/* =========================
   ADICIONAR / REMOVER ITEM
========================= */

function alterarQtd(id, nome, preco, valor) {

    id = String(id); // 🔥 FIX PRINCIPAL

    preco = Number(preco);

    if (!carrinho[id]) {
        carrinho[id] = {
            nome,
            preco,
            quantidade: 0
        };
    }

    carrinho[id].quantidade += valor;

    if (carrinho[id].quantidade < 0) {
        carrinho[id].quantidade = 0;
    }

    atualizarUI(id);
    renderCarrinho();
}


/* =========================
   ATUALIZA QUANTIDADE NA TELA
========================= */

function atualizarUI(id) {

    let el = document.getElementById(`qtd-${id}`);

    if (el) {
        el.innerText = carrinho[id].quantidade;
    }
}


/* =========================
   ATUALIZA CARRINHO COMPLETO
========================= */


/* =========================
   ABRIR CARRINHO
========================= */

function abrirCarrinho() {
    document.getElementById("bottomSheet").classList.add("ativo");
}

function fecharCarrinho() {
    document.getElementById("bottomSheet").classList.remove("ativo");
}

window.addEventListener("click", function (e) {

    let sheet = document.getElementById("bottomSheet");

    if (!sheet) return;

    if (sheet.classList.contains("ativo")) {

        if (!sheet.contains(e.target) && !e.target.closest(".btn-carrinho-fixo")) {
            fecharCarrinho();
        }
    }
});


/* =========================
   FINALIZAR PEDIDO
========================= */

function finalizarPedido() {

    let nome = document.getElementById("nome").value.trim();
    let telefone = document.getElementById("telefone").value.trim();
    let endereco = document.getElementById("endereco").value.trim();

    if (!nome || !telefone || !endereco) {
        mostrarToast("Preencha todos os campos", "error");
        return;
    }

    let itens = [];
    let total = 0;

    for (let id in carrinho) {

        let item = carrinho[id];

        if (item.quantidade > 0) {

            itens.push({
                id: id,
                nome: item.nome,
                quantidade: item.quantidade,
                preco: item.preco
            });

            total += item.preco * item.quantidade;
        }
    }

    if (itens.length === 0) {
        mostrarToast("Carrinho vazio", "error");
        return;
    }

    let pedido = {
        nome,
        telefone,
        endereco,
        itens,
        total
    };

    fetch("/novo-pedido", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pedido)
    })
    .then(res => res.json())
    .then(data => {

        mostrarToast("Pedido enviado com sucesso!", "success");

        carrinho = {};
        renderCarrinho();

        fecharCarrinho();

    })
    .catch(err => {
        console.log(err);
        mostrarToast("Erro ao enviar pedido", "error");
    });
}
/* =========================
   TOAST
========================= */

function mostrarToast(msg, tipo="error"){

    let toast = document.getElementById("toast");

    if(!toast) return;

    toast.className = "toast show " + tipo;

    toast.innerText = msg;

    setTimeout(()=>{

        toast.className = "toast";

    }, 2500);

}


function renderCarrinho() {

    let lista = document.getElementById("listaCarrinho");
    let totalEl = document.getElementById("valorTotal");
    let contadorEl = document.getElementById("contadorCarrinho");

    lista.innerHTML = "";

    let total = 0;
    let contador = 0;

    for (let id in carrinho) {

        let item = carrinho[id];

        if (item.quantidade > 0) {

            contador += item.quantidade;
            total += item.preco * item.quantidade;

            let div = document.createElement("div");
            div.classList.add("item-carrinho");

            div.innerHTML = `
                <div>
                    <strong>${item.nome}</strong><br>
                    <small>${item.quantidade}x R$ ${item.preco.toFixed(2)}</small>
                </div>
                <div>
                    R$ ${(item.preco * item.quantidade).toFixed(2)}
                </div>
            `;

            lista.appendChild(div);
        }
    }

    if (contador === 0) {
        lista.innerHTML = "<p class='vazio'>Carrinho vazio</p>";
    }

    totalEl.innerText = "R$ " + total.toFixed(2);
    contadorEl.innerText = contador;
}

function clicar(el, valor) {

    let id = el.dataset.id;
    let nome = el.dataset.nome;
    let preco = parseFloat(el.dataset.preco);

    alterarQtd(id, nome, preco, valor);
}

