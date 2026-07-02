let carrinho = {};

// =====================================================
// ALTERAR QUANTIDADE
// =====================================================

function alterarQtd(id, nome, preco, valor) {

    if (!carrinho[id]) {
        carrinho[id] = {
            nome,
            preco,
            quantidade: 0
        };
    }

    let antes = carrinho[id].quantidade;

    carrinho[id].quantidade += valor;

    if (carrinho[id].quantidade < 0) {
        carrinho[id].quantidade = 0;
    }

    let depois = carrinho[id].quantidade;

    atualizarInterface(id);
    atualizarTotal();

    if (valor > 0) {
        mostrarToast(`+ ${nome} adicionado`, "success");
    }

    if (valor < 0 && depois > 0) {
        mostrarToast(`- ${nome} removido`, "warning");
    }

    if (antes > 0 && depois === 0) {
        mostrarToast(`${nome} removido do carrinho`, "error");
    }
}

// =====================================================
// INTERFACE
// =====================================================

function atualizarInterface(id) {

    let el = document.getElementById(`qtd-${id}`);

    if (el && carrinho[id]) {
        el.innerText = carrinho[id].quantidade;
    }
}

// =====================================================
// TOTAL
// =====================================================

function atualizarTotal() {

    let total = 0;

    for (let id in carrinho) {
        total += carrinho[id].preco * carrinho[id].quantidade;
    }

    let elTotal = document.getElementById("valorTotal");

    if (elTotal) {
        elTotal.innerText = "R$ " + total.toFixed(2);
    }
}

function calcularTotal() {

    return Object.values(carrinho)
        .reduce((acc, item) => {
            return acc + (item.preco * item.quantidade);
        }, 0);
}

// =====================================================
// FINALIZAR PEDIDO
// =====================================================

function finalizarPedido() {

    let nome = document.getElementById("nome").value;
    let telefone = document.getElementById("telefone").value;
    let endereco = document.getElementById("endereco").value;

    if (!nome || !telefone || !endereco) {
        mostrarToast("Preencha todos os campos", "error");
        return;
    }

    let itens = Object.values(carrinho)
        .filter(i => i.quantidade > 0);

    if (itens.length === 0) {
        mostrarToast("Adicione pelo menos 1 produto", "error");
        return;
    }

    let pedido = {
        nome,
        telefone,
        endereco,
        itens,
        total: calcularTotal()
    };

    enviarPedido(pedido);
}

// =====================================================
// ENVIO (CORRIGIDO)
// =====================================================

function enviarPedido(pedido) {

    fetch("/admin/novo-pedido", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pedido)
    })
    .then(async res => {

        // 🔥 evita erro "Unexpected token <"
        const data = await res.json().catch(() => null);

        if (!res.ok) {
            throw new Error(data?.erro || "Erro no servidor");
        }

        return data;
    })
    .then(data => {

        mostrarToast("Pedido enviado com sucesso!", "success");

        carrinho = {};
        atualizarTotal();

        location.reload();
    })
    .catch(err => {

        console.error(err);

        mostrarToast(err.message || "Erro ao enviar pedido", "error");
    });
}

// =====================================================
// TOAST
// =====================================================

function mostrarToast(mensagem, tipo = "error") {

    let toast = document.getElementById("toast");

    if (!toast) return;

    toast.className = "toast";
    toast.classList.add(tipo);

    toast.innerText = mensagem;

    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 2500);
}

// =====================================================
// FEEDBACK BOTÃO
// =====================================================

function feedbackBotao(id) {

    let btn = document.getElementById(`btn-${id}`);

    if (!btn) return;

    btn.style.transform = "scale(1.2)";

    setTimeout(() => {
        btn.style.transform = "scale(1)";
    }, 150);
}