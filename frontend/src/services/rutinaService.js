// src/services/rutinaService.js
const API_URL = 'http://127.0.0.1:8000/api'

const generarRutinas = async () => {
  const token = localStorage.getItem('token')
  const respuesta = await fetch(`${API_URL}/rutinas/generar`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  
  if (!respuesta.ok) {
    const errorData = await respuesta.json()
    throw new Error(errorData.detail || 'Error al generar la rutina')
  }
  return await respuesta.json()
}

const votarRutina = async (votoData) => {
  const token = localStorage.getItem('token')
  const respuesta = await fetch(`${API_URL}/rutinas/votar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(votoData)
  })

  if (!respuesta.ok) throw new Error('Error al registrar el voto')
  return await respuesta.json()
}

// Añade esta función a tu rutinaService.js
const generarRutinaFase2 = async (usuarioData) => {
  try {
    // 1. Cogemos la pulsera VIP
    const token = localStorage.getItem('token') 
    
    // 2. Usamos tu API_URL para que sea igual que las otras
    const response = await fetch(`${API_URL}/rutinas/generar-inteligente`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}` // 3. ¡Descomentado y funcionando!
      },
      body: JSON.stringify(usuarioData)
    });

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Error al generar la rutina inteligente');
    }

    return await response.json();
  } catch (error) {
    throw error;
  }
};

const votarFase2 = async (votoData) => {
  const token = localStorage.getItem('token')
  const respuesta = await fetch(`${API_URL}/rutinas/votar-fase2`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(votoData)
  })

  if (!respuesta.ok) {
    // En lugar de lanzar un error genérico, leemos la respuesta real
    const errorData = await respuesta.json()
    throw new Error(errorData.detail || 'Error desconocido en el servidor')
  }
  return await respuesta.json()
}


export default { generarRutinas, votarRutina, generarRutinaFase2,votarFase2 }