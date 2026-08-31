// src/services/authService.js

const API_URL = 'http://127.0.0.1:8000/api'

const login = async (email, password) => {
  const respuesta = await fetch(`${API_URL}/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  
  const datos = await respuesta.json()
  
  if (!respuesta.ok) {
    throw new Error(datos.detail || 'Error en el login')
  }
  return datos
}

const registro = async (nombre, email, password) => {
  const respuesta = await fetch(`${API_URL}/auth/registro`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre, email, password })
  })
  
  const datos = await respuesta.json()
  
  if (!respuesta.ok) {
    throw new Error(datos.detail || 'Error en el registro')
  }
  return datos
}

export default { login, registro }