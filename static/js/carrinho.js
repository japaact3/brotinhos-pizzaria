let carrinho = {};

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

    // 🔥 FEEDBACK EM TEMPO REAL

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





function atualizarInterface(id) {

    let el = document.getElementById(`qtd-${id}`);

    if (el) {
        el.innerText = carrinho[id].quantidade;
    }
}

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

    let total = 0;

    for (let id in carrinho) {

        if (carrinho[id].quantidade > 0) {
            total += carrinho[id].preco * carrinho[id].quantidade;
        }

    }

    return total;
}


function finalizarPedido() {

    let nome = document.getElementById("nome").value;
    let telefone = document.getElementById("telefone").value;
    let endereco = document.getElementById("endereco").value;

    // 🚨 validação
    if (!nome) {
        mostrarToast("Digite o nome do cliente", "error");
        return;
    }

    if (!telefone) {
        mostrarToast("Digite o telefone", "error");
        return;
    }

    if (!endereco) {
        mostrarToast("Digite o endereço", "error");
        return;
    }

    let itens = [];

    for (let id in carrinho) {
        if (carrinho[id].quantidade > 0) {
            itens.push(carrinho[id]);
        }
    }

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






function enviarPedido(pedido) {

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

        // limpa carrinho
        carrinho = {};
        atualizarTotal();

        // recarrega página (opcional)
        location.reload();

    })
    .catch(err => {
        mostrarToast("Erro ao enviar pedido:", "error");
    });
}

function mostrarToast(mensagem, tipo = "error") {

    let toast = document.getElementById("toast");

    // limpa classes antigas
    toast.className = "toast";

    // adiciona tipo
    toast.classList.add(tipo);

    // texto
    toast.innerText = mensagem;

    // mostra
    toast.classList.add("show");

    // remove automático
    setTimeout(() => {
        toast.classList.remove("show");
    }, 2500);
}

function feedbackBotao(id) {

    let btn = document.getElementById(`btn-${id}`);

    if (!btn) return;

    btn.style.transform = "scale(1.2)";

    setTimeout(() => {
        btn.style.transform = "scale(1)";
    }, 150);
}
