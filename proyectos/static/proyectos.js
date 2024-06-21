function generar_reporte_granulometria(event, id_proyecto){
    
    axios.get(obtener_ReportesURL, {
        params: {
            id_proyecto: id_proyecto
        }
        })
        .then(function (response) {
            const reportes = response.data;

            console.log(reportes);

            // Iterar sobre cada objeto en el array recibido
            reportes.forEach(function (factor) {
                
            });

            return "se logro";
        })
        .catch(function (error) {
            console.log('Error:', error);
        });
}