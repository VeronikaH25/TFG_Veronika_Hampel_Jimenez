// src/services/userService.js
const API_URL = 'http://127.0.0.1:8000/api'

const obtenerPerfil = async () => {
  const token = localStorage.getItem('token')
  const respuesta = await fetch(`${API_URL}/usuarios/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  if (!respuesta.ok) throw new Error('No se pudo obtener el perfil')
  return await respuesta.json()
}


const actualizarPerfil = async (datos) => {
  const token = localStorage.getItem('token');
  const respuesta = await fetch(`${API_URL}/usuarios/actualizar`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(datos)
  });

  if (!respuesta.ok) throw new Error('Error al actualizar el perfil');
  return await respuesta.json();
};

export default { obtenerPerfil, actualizarPerfil }; 