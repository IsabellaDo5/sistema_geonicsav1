function graficar(event) {
    const mallas_medidas = document.getElementsByName("PRPMM");
    const pesos_t1 = document.getElementsByName("PQP");
    const pesos_t2 = document.getElementsByName("PQPL");


    let mallas_lista = [];
    let pesos_lista = [];
    let contador_t2 = 0;

    for (let i = 0; i < mallas_medidas.length; i++) {
        if (mallas_medidas[i].value && mallas_medidas[i].value > 2 && mallas_medidas[i].value != 5) {
            mallas_lista.push(mallas_medidas[i].value.trim());
            pesos_lista.push(pesos_t1[i].value.trim());
        }
        else if(mallas_medidas[i].value && mallas_medidas[i].value <= 2 && mallas_medidas[i].value != 0.08){
            mallas_lista.push(mallas_medidas[i].value.trim());
            pesos_lista.push(pesos_t2[contador_t2].value.trim());
            contador_t2 += 1;
        }
        
    }

    GraficaItemsMasVendidos(mallas_lista, pesos_lista, document.getElementById("granulometria_chart"))
}
/*
axios.get('/ajax/obtener_grafica/', {
        params: {
            mallas_lista: JSON.stringify(mallas_lista),
            pesos_lista: JSON.stringify(pesos_lista)
        },
        responseType: 'blob'
    })
        .then(function (response) {

            console.log(response.data);
            const url = URL.createObjectURL(response.data);
            document.getElementById('grafica').src = url;
        })
        .catch(function (error) {
            console.error('Error al obtener la gráfica:', error);
        });
*/
function calcTabla1(event, prp, perp, pera, pqp, sumaprp, sumaperp) {
    calcularPeRP(prp, perp, sumaprp, sumaperp);
    calcularPeRA(perp, pera);
    calcularPQP(pera, pqp);
}

function calcTabla2(event, prp, perp, pera, pqp, sumaprp, sumaperp) {
    calcularPeRPL(prp, perp, sumaprp, sumaperp);
    calcularPeRA(perp, pera);
    calcularPQPL(pera, pqp);
    tabla_lavado();
    fracciones_muestra();
}


function fracciones_muestra() {
    const pct_grava = document.getElementById("PCEG_GRANULOMETRIA");
    const pct_arena = document.getElementById("PCEA_GRANULOMETRIA");
    const pct_fino = document.getElementById("PCEF_GRANULOMETRIA");


    pct_grava.textContent = 100 - parseFloat(document.getElementById("PQP9").value);
    pct_fino.textContent = parseFloat(document.getElementById("PQPL12").value);
    pct_arena.textContent = 100 - (parseFloat(pct_grava.textContent) + parseFloat(pct_fino.textContent));
}
function tabla_lavado() {

    const peso_seco = document.getElementById("PS_GRANULOMETRIA");
    const diferencia = document.getElementById("DIF_GRANULOMETRIA");
    const peso_seco_lavado = document.getElementById("PSL_GRANULOMETRIA");


    peso_seco.value = document.getElementById("sumaPRPL").textContent;
    diferencia.textContent = document.getElementById("PRPL14").value;
    peso_seco_lavado.textContent = parseFloat(peso_seco.value) - parseFloat(diferencia.textContent);

}
function calcularPeRP(prp, perp, sumaPRP, sumaperp) {

    console.log(prp, perp, sumaperp, sumaPRP);
    const PRPInput = document.getElementsByName(prp);
    const PeRPInput = document.getElementsByName(perp);
    let sumarPRP = document.getElementById(sumaPRP).textContent;
    const totalPeRP = document.getElementById(sumaperp);
    let sumador = 0.0;


    for (let x = 0; x < PRPInput.length; x++) {
        PeRPInput[x].value = "";
        const value = PRPInput[x].value;
        if (value !== "") {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                PeRPInput[x].value = Math.round((PRPInput[x].value * 100) / sumarPRP);
                sumador += parseFloat(PeRPInput[x].value);
            }
        }

        totalPeRP.textContent = sumador;

    }
}
function calcularPeRPL(prp, perp, sumaPRP, sumaperp) {

    console.log(prp, perp, sumaperp, sumaPRP);
    const PRPInput = document.getElementsByName(prp);
    const PeRPInput = document.getElementsByName(perp);
    let sumarPRP = document.getElementById(sumaPRP).textContent;
    const totalPeRP = document.getElementById(sumaperp);
    const pqp_t1 = document.getElementById("PQP9");
    let sumador = 0.0;


    for (let x = 0; x < PRPInput.length; x++) {
        PeRPInput[x].value = "";
        const value = PRPInput[x].value;
        if (value !== "") {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                PeRPInput[x].value = Math.round(peso/sumarPRP*pqp_t1.value);
                sumador += parseFloat(PeRPInput[x].value);
            }
        }

        totalPeRP.textContent = sumador;

    }
}

function calcularPeRA(perp_, pera_) {
    const PeRP = document.getElementsByName(perp_);
    const PeRA = document.getElementsByName(pera_);
    let sumador = 0.0;

    for (let x = 0; x < PeRP.length; x++) {
        PeRA[x].value = "";
        let value = PeRP[x].value;

        if (value !== "") {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                sumador += peso;
                PeRA[x].value = Math.round(sumador);
            }
        }
    }
}

function calcularPQP(pera_, pqp_) {

    const PeRA = document.getElementsByName(pera_);
    const PQP = document.getElementsByName(pqp_);
    const prpmm = document.getElementsByName("PRPMM");
    const id = document.getElementsByName("ID_MALLA");

    for (let x = 0; x < PeRA.length; x++) {
        PQP[x].value = "";
        let value = PeRA[x].value;

        if (prpmm[x].value && value !== "" && id[x].value < 13) {
            const peso = parseFloat(value);
            if (!isNaN(peso)) {
                PQP[x].value = Math.round(100 - peso);
            }
            
        }
        else if(prpmm[x].value && id[x].value < 13){
            PQP[x].value = 100;
        }
    }

}

function calcularPQPL(pera_, pqp_) {

    const PeRA = document.getElementsByName(pera_);
    const PQP = document.getElementsByName(pqp_);
    const prpmm = document.getElementsByName("PRPMM");
    const pqp_t1 = document.getElementById("PQP9");
    const id = document.getElementsByName("ID_MALLA");

    let contador = 10;
    for (let x = 0; x < PeRA.length; x++) {
        PQP[x].value = "";
        let valor = PeRA[x].value;
        console.log(valor);
        if (prpmm[contador].value && valor != "" && id[x].value < 13) {
            const peso = parseFloat(valor);

            console.log(prpmm[contador].value);
            if (!isNaN(peso)) {
                PQP[x].value = Math.round(pqp_t1.value - peso);
            }
            
        }
        else if(prpmm[contador].value && id[x].value < 13){
            PQP[x].value = 100;
        }
        contador +=1;
    }

}
function sumaPRP(event, PRP, sumaPRP_) {
    const PRP_lista = document.getElementsByName(PRP);
    let sumaPRP = document.getElementById(sumaPRP_);
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

// GRAFICAR
function GraficaItemsMasVendidos(x_label, y_label, ctx) {
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: x_label,
            datasets: [
                {
                    label: "% que pasa",
                    backgroundColor: escogerColor(),
                    borderColor: escogerColor(),
                    data: y_label
                }
            ]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Curva Granulometrica' // Puedes personalizar este texto
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Mallas(mm)' // Título del eje X
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: '% que pasa' // Título del eje Y
                    }
                }
            },
            
        }
    });
}


function escogerColor() {
    var colorList = ["#a2d2ff", "#d62828", "#0077b6", "#83c5be", "#e76f51"];

    
    if (colorList && colorList.length > 0) {
        // Generar un número aleatorio entre 0 y la longitud de la lista de colores
        var randomIndex = Math.floor(Math.random() * colorList.length);
        // Devolver el color seleccionado aleatoriamente
        return colorList[randomIndex];
    } else {
        // Si la lista de colores está vacía, devolver un mensaje de error
        return "Error: La lista de colores está vacía";
    }
}

