
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

function activar_orden(orden_id, buttonElement) {
    axios.post(activar_orden_url, {
      id_orden: orden_id
    }, {
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    })
    .then(function (response) {
      console.log('Funcionó', response.data);
      // Aquí puedes agregar lógica para actualizar la interfaz, por ejemplo:
      buttonElement.textContent = 'Activada';
      buttonElement.classList.remove('btn-danger');
      buttonElement.classList.add('btn-secondary');
      buttonElement.onclick = null;  // Desactivar el botón
    })
    .catch(function (error) {
      console.log('Error:', error);
    });
  }

  
  function desactivar_orden(orden_id, buttonElement) {
    axios.post(orden_url, {
      id_orden: orden_id
    }, {
      headers: {
        'X-CSRFToken': getCsrfToken()
      }
    })
    .then(function (response) {
      console.log('Funcionó', response.data);
      // Aquí puedes agregar lógica para actualizar la interfaz, por ejemplo:
      buttonElement.textContent = 'Desactivado';
      buttonElement.classList.remove('btn-danger');
      buttonElement.classList.add('btn-secondary');
      buttonElement.onclick = null;  // Desactivar el botón
    })
    .catch(function (error) {
      console.log('Error:', error);
    });
  }  