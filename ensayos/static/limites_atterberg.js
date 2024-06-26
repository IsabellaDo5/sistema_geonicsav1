function obtenerFactor(no_golpes_id, factor_id){
    const no_golpes = document.getElementById(no_golpes_id).value;
    const factor_input = document.getElementById(factor_id);

    axios.get(obtenerFactoresUrl)
        .then(function (response) {
            const catalogo_factores = response.data;

            // Limpiar el contenedor antes de imprimir el factor
            factor_input.value="";

            // Iterar sobre cada objeto en el array recibido
            catalogo_factores.forEach(function (factor) {
                if( no_golpes== factor.N ){
                    factor_input.value = factor.K;
                }
            });

            return factor_input.value;
        })
        .catch(function (error) {
            console.log('Error:', error);
        });
        
}
function limite_liquido(event, no_golpes, no_recipiente, pw_recip, ps_recip, agua, recipiente, peso_seco, pte_agua, factor, ll_input) {
    calcular_agua(pw_recip, ps_recip, agua);
    calcular_peso_seco(ps_recip, recipiente, peso_seco);
    calcular_pte_agua(agua, peso_seco, pte_agua);
    calcular_limite_liquido(factor, pte_agua, ll_input);
    calcular_LLpromedio();
}

function limite_plastico(event, pw_recip, ps_recip, agua, recipiente, peso_seco_lp, lp_input) {
    calcular_agua(pw_recip, ps_recip, agua);
    calcular_peso_seco(ps_recip, recipiente, peso_seco_lp);
    calcular_limite_plastico(agua, peso_seco_lp, lp_input);
}


function calcular_limite_liquido(factor_input, pte_agua, ll_input){
    const factor = document.getElementsByName(factor_input)
    const pce_agua = document.getElementsByName(pte_agua);
    const LL = document.getElementsByName(ll_input)


    for (let x = 0; x < pce_agua.length; x++) {
        LL[x].value = "";
        const factor_value = factor[x].value;
        const pte_agua = pce_agua[x].value;

        if (factor_value !== "" && pte_agua != "") {
            const arg1 = parseFloat(factor_value);
            const arg2 = parseFloat(pte_agua);
            if (!isNaN(arg1) && !isNaN(arg2)) {
                LL[x].value = (arg1*arg2).toFixed(2);
            }
        }
    }
}


function calcular_limite_plastico(agua_input, peso_seco_input, LP_input){
    const agua_tag = document.getElementsByName(agua_input);
    const ps_tag = document.getElementsByName(peso_seco_input);
    const lp_tag = document.getElementsByName(LP_input);

    for (let x = 0; x < agua_tag.length; x++) {
        lp_tag[x].value = "";
        const agua = agua_tag[x].value;
        const ps = ps_tag[x].value;

        if (agua !== "" && ps != "") {
            const arg1 = parseFloat(agua);
            const arg2 = parseFloat(ps);
            if (!isNaN(arg1) && !isNaN(arg2)) {
                lp_tag[x].value = (100*(arg1/arg2)).toFixed(2);
            }
        }
    }

}

function calcular_peso_seco(ps_mas_recip, recipiente_input, peso_seco) {
    const ps_recip = document.getElementsByName(ps_mas_recip);
    const recipiente = document.getElementsByName(recipiente_input);
    const resultado_input = document.getElementsByName(peso_seco);

    for (let x = 0; x < ps_recip.length; x++) {
        resultado_input[x].value = "";
        const ps = ps_recip[x].value;
        const recip = recipiente[x].value;

        if (recip !== "" && ps !== "") {
            const arg1 = parseFloat(ps);
            const arg2 = parseFloat(recip);
            if (!isNaN(arg1) && !isNaN(arg2)) {
                resultado_input[x].value = (arg1 - arg2).toFixed(2);
            }
        }
    }
}
function calcular_agua(pw_mas_recip, ps_mas_recip, agua) {

    const pw_recip = document.getElementsByName(pw_mas_recip);
    const ps_recip = document.getElementsByName(ps_mas_recip);
    const agua_input = document.getElementsByName(agua);

    for (let x = 0; x < pw_recip.length; x++) {
        agua_input[x].value = "";
        const pw = pw_recip[x].value;
        const ps = ps_recip[x].value;

        if (pw !== "" && ps != "") {
            const arg1 = parseFloat(pw);
            const arg2 = parseFloat(ps);
            if (!isNaN(arg1) && !isNaN(arg2)) {
                agua_input[x].value = (arg1 - arg2).toFixed(2);

                console.log(pw, ps + " Args: " + arg1, arg2);
                console.log(agua_input[x].value)
            }
        }
    }
}

function calcular_pte_agua(agua_i, peso_seco_i, pct_agua_i) {
    const agua = document.getElementsByName(agua_i);
    const pesoseco = document.getElementsByName(peso_seco_i);
    const pce_agua = document.getElementsByName(pct_agua_i);

    for (let x = 0; x < agua.length; x++) {
        pce_agua[x].value = "";
        const a = agua[x].value;
        const ps = pesoseco[x].value;

        if (a !== "" && ps != "") {
            const arg1 = parseFloat(a);
            const arg2 = parseFloat(ps);
            if (!isNaN(arg1) && !isNaN(arg2)) {
                pce_agua[x].value = (100 * (arg1 / arg2)).toFixed(2);
            }
        }
    }

}

function calcular_LLpromedio(){
    let resultado = document.getElementById("LL_promedio");
    const LL = document.getElementsByName("Limite_liquido");
    let suma = 0;
    let x = 0;

    for(x = 0;x<LL.length; x++){
        suma += parseFloat(LL[x].value);

    }
    console.log(suma);
    resultado.value = suma/LL.length;
}

function calcular_LPpromedio(){
    let resultado = document.getElementById("LP_promedio");
    const LP = document.getElementsByName("Limite_Plastico");
    let suma = 0;
    let x = 0;

    for(x = 0;x<LP.length; x++){
        suma += parseFloat(LP[x].value);

    }
    console.log(suma);
    resultado.value = suma/LP.length;
}
function obtenerDatosCF(){
    const y_label = document.getElementsByName("Limite_liquido");
    const x_label = document.getElementsByName("no_golpes_LL");

    var arr_xlabel = [];
    var arr_ylabel = [];

    for(var i = 0; i < x_label.length; ++i){
        console.log("X label: " + x_label[i].value);
        arr_xlabel.push(x_label[i].value);
        console.log("Y label: " + y_label[i].value);
        arr_ylabel.push(y_label[i].value);
    } 
    
    console.log("X label array: " + arr_xlabel);
    console.log("Y label array: " + arr_ylabel);
    curvaFluidez(arr_xlabel, arr_ylabel, document.getElementById("CFluidez"));
}


function curvaFluidez(x_label, y_label, ctx) {
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: x_label,
            datasets: [
                {
                    label: "Limite liquido",
                    backgroundColor: escogerColor(),
                    borderColor: escogerColor(),
                    data: y_label,
                    fill: false,
                    pointStyle: 'circle',
                    pointRadius: 10,
                    pointHoverRadius: 15
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Curva de Fluidez' // Puedes personalizar este texto
                }
            },
            scales: {
                x: {
                    type: 'linear', // Asegúrate de que el tipo de eje sea 'linear'
                    display: true,
                    title: {
                        display: true,
                        text: 'No. de golpes' // Título del eje X
                    },
                    min: 0, // Configura el mínimo valor del eje X
                    ticks: {
                        stepSize: 10 // Define el tamaño de los pasos en el eje X
                    }
                },
                y: {
                    display: true,
                    beginAtZero: true, // Asegura que el eje Y comience en 0
                    title: {
                        display: true,
                        text: 'Limite liquido' // Título del eje Y
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