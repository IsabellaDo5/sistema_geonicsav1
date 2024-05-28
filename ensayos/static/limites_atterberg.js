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
function limite_liquido(event, no_golpes, no_recipiente, pw_recip, ps_recip, agua, recipiente, peso_seco, pte_agua, factor) {
    calcular_agua(pw_recip, ps_recip, agua);
    calcular_peso_seco(ps_recip, recipiente, peso_seco);
    calcular_pte_agua(agua, peso_seco, pte_agua);
}

function limite_plastico(event, pw_recip, ps_recip, agua, recipiente, peso_seco, pte_agua, factor){
    calcular_agua(pw_recip, ps_recip, agua);
}
function calcular_peso_seco(ps_mas_recip, recipiente_input, peso_seco) {
    const ps_recip = document.getElementsByName(ps_mas_recip);
    const recipiente = document.getElementsByName(recipiente_input);
    const resultado_input = document.getElementsByName(peso_seco);

    for (let x = 0; x < ps_recip.length; x++) {
        resultado_input[x].value = "";
        const ps = ps_recip[x].value;
        const recip = recipiente[x].value;

        if (recip !== "" && ps != "") {
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