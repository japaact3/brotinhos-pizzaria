



function atualizarCampo() {

    let texto = [];
    

    for (let sabor in itens) {
        if (itens[sabor] > 0) {
            texto.push(sabor + ":" + itens[sabor]);
            resumo.push(itens[sabor] + "x " + sabor);
        }
    }

    document.getElementById("itens").value = texto.join(", ");

    document.getElementById("resumoSabores").innerText =
        resumo.length > 0 ? resumo.join(" | ") : "Nenhum sabor selecionado";
}


function alterarStatus(id, status){

    fetch(`/atualizar-status/${id}`, {

        method: "POST",

        headers:{
            "Content-Type":"application/json"
        },

        body: JSON.stringify({
            status: status
        })

    })
    .then(res => res.json())
    .then(() => {

        location.reload();

    })
    .catch(err => {

        console.error(err);

        alert("Erro ao atualizar o pedido.");

    });

}