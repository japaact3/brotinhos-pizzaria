function atualizarCampo() {

    let texto = [];
    let resumo = []; // ✅ corrigido (antes estava faltando)

    for (let sabor in itens) {

        if (itens[sabor] > 0) {

            texto.push(`${sabor}:${itens[sabor]}`);

            resumo.push(`${itens[sabor]}x ${sabor}`);
        }
    }

    let inputItens = document.getElementById("itens");
    let resumoEl = document.getElementById("resumoSabores");

    if (inputItens) {
        inputItens.value = texto.join(", ");
    }

    if (resumoEl) {
        resumoEl.innerText =
            resumo.length > 0
                ? resumo.join(" | ")
                : "Nenhum sabor selecionado";
    }
}

// =====================================================
// ALTERAR STATUS (CORRIGIDO)
// =====================================================

function alterarStatus(id, status) {

    fetch(`/api/status/${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            status: status
        })
    })
    .then(async res => {

        const data = await res.json().catch(() => null);

        if (!res.ok) {
            throw new Error(data?.erro || "Erro ao atualizar status");
        }

        return data;
    })
    .then(() => {

        location.reload();
    })
    .catch(err => {

        console.error(err);

        alert(err.message || "Erro ao atualizar o pedido.");
    });
}

function atualizarPedidos() {

    

    fetch("/api/pedidos")
        .then(res => res.json())
        .then(data => {


            data.forEach(pedido => {

                let card = document.getElementById(`pedido-${pedido.id}`);

                if (!card) return;

                let statusEl = card.querySelector(".status");

                if (!statusEl) return;

                // 🔥 só anima se o status mudou
                if (statusEl.innerText !== pedido.status) {

                    statusEl.innerText = pedido.status;

                    // =========================
                    // ANIMAÇÃO VISUAL
                    // =========================

                    statusEl.style.transition = "0.3s";
                    statusEl.style.transform = "scale(1.3)";
                    statusEl.style.fontWeight = "bold";

                    // cores por status (opcional mas recomendado)
                    if (pedido.status.includes("preparo")) {
                        statusEl.style.color = "#f1c40f";
                    }

                    if (pedido.status.includes("Pronto")) {
                        statusEl.style.color = "#2ecc71";
                    }

                    if (pedido.status.includes("entrega")) {
                        statusEl.style.color = "#3498db";
                    }

                    if (pedido.status.includes("Entregue")) {
                        statusEl.style.color = "#27ae60";
                    }

                    if (pedido.status.includes("Cancelado")) {
                        statusEl.style.color = "#e74c3c";
                    }

                    // volta ao normal
                    setTimeout(() => {
                        statusEl.style.transform = "scale(1)";
                    }, 300);
                }
            });
           })
        .catch(err => {
            console.error("Erro ao atualizar pedidos:", err);
        });
}

// roda a cada 3 segundos
setInterval(atualizarPedidos, 3000);
atualizarPedidos()
