function generar_reporte_granulometria(event, id_proyecto){
    let obtener_ReportesURL = "{% url 'obtener_reporte_GL' %}";
    
    axios.get(obtener_ReportesURL, {
        params: {
            id_proyecto: id_proyecto
        }
        })
        .then(function (response) {
            const reportes = response.data;

            // Limpiar el contenedor antes de imprimir el factor
            factor_input.value="";

            // Iterar sobre cada objeto en el array recibido
            reportes.forEach(function (factor) {
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