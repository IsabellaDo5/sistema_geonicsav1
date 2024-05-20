function calcTabla1(event){
    calcularPeRP();
    calcularPeRA();
    calcularPQP();
}


function calcularPeRP() {

    const PRPInput = document.getElementsByName("PRP");
    const PeRPInput = document.getElementsByName("PeRP");
    let sumarPRP =document.getElementById("sumaPRP").textContent;
    const totalPeRP = document.getElementById("sumaPeRP");
    let sumador = 0.0;


    for (let x = 0; x < PRPInput.length; x++) {
        PeRPInput[x].value="";
        const value = PRPInput[x].value;
        if (value !== "") {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                PeRPInput[x].value= ((PRPInput[x].value * 100)/sumarPRP).toFixed(3);
                sumador += parseFloat(PeRPInput[x].value);
            }
        }
    
    totalPeRP.textContent = sumador;

}}


function calcularPeRA(){
    const PeRP = document.getElementsByName("PeRP");
    const PeRA = document.getElementsByName("PeRA");
    let sumador = 0.0;

    for (let x = 0; x < PeRP.length; x++) {
        PeRA[x].value="";
        let value = PeRP[x].value;

        if (value !== "") {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                sumador += peso;
                PeRA[x].value = sumador.toFixed(3);
            }
        }
    }
}

function calcularPQP(){

    const PeRA = document.getElementsByName("PeRA");
    const PQP = document.getElementsByName("PQP");
    for (let x = 0; x < PeRA.length; x++) {
        PQP[x].value="";
        let value = PeRA[x].value;

        if (value !== "") {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                PQP[x].value = (100-peso).toFixed(3);
            }
        }
    }

}
function sumaPRP(event) {
    const PRP_lista = document.getElementsByName("PRP");
    let sumaPRP = document.getElementById("sumaPRP");
    let sumador = 0.0;

    for (let x = 0; x < PRP_lista.length; x++) {
        const value = PRP_lista[x].value;
        if (value !== "") {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                sumador += peso;
            }
        }
    }
    
    sumaPRP.textContent = sumador.toFixed(3); // Formatea el resultado a dos decimales

}
