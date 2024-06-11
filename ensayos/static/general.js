function obtenerCliente(proyecto_nombre, cliente_input){
    const proyecto = document.getElementById(proyecto_nombre).value;
    const cliente = document.getElementById(cliente_input);

    axios.get(obtenerClienteUrl, {
        params: {
            proyecto: proyecto
        }
    })
    .then(function (response) {
        const catalogo_factores = response.data;

        // Limpiar el contenedor antes de imprimir el cliente
        cliente.value = "";

        // Iterar sobre cada objeto en el array recibido
        catalogo_factores.forEach(function (info) {
            cliente.value = info.cliente;
        });

        return cliente.value;
    })
    .catch(function (error) {
        console.log('Error:', error);
    });
}