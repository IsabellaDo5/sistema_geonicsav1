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
        else if (mallas_medidas[i].value && mallas_medidas[i].value <= 2 && mallas_medidas[i].value != 0.08) {
            mallas_lista.push(mallas_medidas[i].value.trim());
            pesos_lista.push(pesos_t2[contador_t2].value.trim());
            contador_t2 += 1;
        }

    }

    curvaGranulometrica(mallas_lista, pesos_lista, document.getElementById("granulometria_chart"))
}

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
    diferencia.textContent = document.getElementById("PRPL15").value;
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
                PeRPInput[x].value = Math.round(peso / sumarPRP * pqp_t1.value);
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
        else if (prpmm[x].value && id[x].value < 13) {
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
        else if (prpmm[contador].value && id[x].value < 13) {
            PQP[x].value = 100;
        }
        contador += 1;
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
function curvaGranulometrica(x_label, y_label, ctx) {
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: x_label,
            datasets: [
                {
                    label: "% que pasa",
                    backgroundColor: escogerColor(),
                    borderColor: escogerColor(),
                    data: y_label,
                    fill: false
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
                    type: 'logarithmic', // Cambia el tipo de escala a logarítmica
                    display: true,
                    reverse: true,
                    suggestedMax: 100,
                    title: {
                        display: true,
                        text: 'Mallas(mm)' // Título del eje X
                    }
                },
                y: {
                    display: true,
                    suggestedMin: 0,
                    title: {
                        display: true,
                        text: '% que pasa' // Título del eje Y
                    }
                }
            }
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
        
        return "Error: La lista de colores está vacía";
    }
}

function lista_porcentaje_pasa() {
    let pce_pasa = document.getElementsByName("PQP");
    let pce_pasa_lavado = document.getElementsByName("PQPL");
    let lista_completa = [];
    let y = 0;
    for (let x = 0; x <= 14; x++) {


        try {
            lista_completa.push(pce_pasa[x].value)
        }
        catch {
            try {
                lista_completa.push(pce_pasa_lavado[y].value)
                y++;
            }
            catch {
                console.log("Error: El elemento en nodelist tenia value vacio.");
            }

        }
    }
    console.log(lista_completa);
    return lista_completa;
}

function calcular_cu() {

    const contenedor = document.getElementById("tabla_coeficientes");
    let lista_mallas = lista_de_mallas()

    let resultado_d10 = 0.0;
    let resultado_d30 = 0.0;
    let resultado_d60 = 0.0;
    let cu = 0.0;
    let cc = 0.0;

    // calcular D10
    let lista_pce = lista_porcentaje_pasa();
    let menor = menor_masCercano(lista_pce, lista_mallas, 10);
    let mayor = mayor_masCercano(lista_pce, lista_mallas, 10);
    console.log("D10: menor: " + menor + " mayor: " + mayor)

    resultado_d10 = calcular_d_x(mayor, menor, 10);
    console.log("RESULTADO D10: " + resultado_d10);

    // calcular D30
    menor = menor_masCercano(lista_pce, lista_mallas, 30);
    mayor = mayor_masCercano(lista_pce, lista_mallas, 30);
    console.log("D30: menor: " + menor + " mayor: " + mayor)
    resultado_d30 = calcular_d_x(mayor, menor, 30);
    console.log("RESULTADO D30: " + resultado_d30);

    // calcular D60
    menor = menor_masCercano(lista_pce, lista_mallas, 60);
    mayor = mayor_masCercano(lista_pce, lista_mallas, 60);
    resultado_d60 = calcular_d_x(mayor, menor, 60);
    console.log("RESULTADO D60: " + resultado_d60);
    cu = resultado_d60 / resultado_d10;
    cc = Math.pow(resultado_d30, 2) / (resultado_d60 * resultado_d10);

    contenedor.innerHTML = `
    <table class="table table-bordered border-dark-subtle">
  <tbody>
    <tr>
    <th scope="col">D10</th>
    <td > <input class="form-control-plaintext" name = "d10" type="text" value=" `+ resultado_d10 + `" aria-label="Disabled input example" disabled readonly></td>
      
    </tr>
    
    <tr>
        <th scope="col">D30</th>
        <td > <input class="form-control-plaintext" name = "d30" type="text" value=" `+ resultado_d30 + `" aria-label="Disabled input example" disabled readonly></td>
    </tr>
    <tr>
        <th scope="col">D60</th>
        <td > <input class="form-control-plaintext" name = "d60" type="text" value=" `+ resultado_d60 + `" aria-label="Disabled input example" disabled readonly></td>

    </tr>

    <tr>
    <th scope="col" class="table-active">Coeficiente de uniformidad (Cu):</th>
    <td class="table-active"> <input class="form-control-plaintext" type="text" name="cu" value="`+ cu.toFixed(3) + `" aria-label="Disabled input example" disabled readonly></td>
      
    </tr>
    
    <tr>
        <th scope="col" class="table-active">Coeficiente de curvatura</th>
        <td class="table-active"> <input class="form-control-plaintext" type="text" name="cc" value="`+ cc.toFixed(3) + `" aria-label="Disabled input example" disabled readonly></td> 
    </tr>
  </tbody>
</table>
    `

}


function calcular_d_x(d1_, d2_, x) {
    let dx = 0.0;
    let d1 = parseFloat(d1_[0]);
    let d2 = parseFloat(d2_[0]);

    let d1_pce = parseFloat(d1_[1]);
    let d2_pce = parseFloat(d2_[1]);

    if (d1 && d2) {

        dx = ((d2 - d1) / ( (d2_pce) -  (d1_pce))).toFixed(3) * ( (parseFloat(x)) -  (d1_pce)).toFixed(3) + d1;
    }

    return dx.toFixed(3);
}

function lista_de_mallas() {
    let lista_de_mallas = document.getElementsByName("PRPMM");
    let lista_completa = [];
    let y = 0;
    for (let x = 0; x <= 14; x++) {


        try {
            lista_completa.push(lista_de_mallas[x].value)
        }
        catch {

        }
    }
    console.log(lista_completa);

    return lista_completa;
}

function menor_masCercano(pce_pasa, prp, num) {

    let cercano = 0;
    let diferencia = 100;
    let d2 = 0;

    let info_menor = []
    for (let i = 0; i < pce_pasa.length; i++) {

        if (pce_pasa != "") {
            if (pce_pasa[i] == num) {
                cercano = pce_pasa[i];
                d2 = prp[i];
            }
            else if (pce_pasa[i] < num) {
                if (Math.abs(pce_pasa[i] - num) < diferencia) {
                    cercano = pce_pasa[i];
                    d2 = prp[i];
                    diferencia = Math.abs(pce_pasa[i] - num);
                }
            }
        }

    }
    info_menor.push(d2);
    info_menor.push(cercano);

    return info_menor;
}
// NUmero mayor más cercano
function mayor_masCercano(pce_pasa, prp, num) {

    let cercano = 0;
    let diferencia = 100;
    let d1 = 0;

    let info_mayor = []
    for (let i = 0; i < pce_pasa.length; i++) {

        if (pce_pasa != "") {

            if (pce_pasa[i] > num) {
                if (diferencia == 0) {
                    i += 1;
                }
                else if (Math.abs(pce_pasa[i] - num) < diferencia) {
                    cercano = pce_pasa[i];
                    d1 = prp[i];
                    diferencia = Math.abs(pce_pasa[i] - num);
                }

            }

        }

    }
    info_mayor.push(d1);
    info_mayor.push(cercano);

    return info_mayor;
}


