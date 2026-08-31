// src/controllers/useAuthController.js
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import authService from '../services/authService'

export const useAuthController = () => {
  const [errorBackend, setErrorBackend] = useState('')
  const navigate = useNavigate()

  const ejecutarLogin = async (email, password) => {
    setErrorBackend('')
    try {
      const datos = await authService.login(email, password)
      localStorage.setItem('token', datos.access_token)
      localStorage.setItem('nombre', datos.usuario_nombre)
      navigate('/dashboard')
    } catch (error) {
      setErrorBackend(error.message)
    }
  }

  const ejecutarRegistro = async (nombre, email, password, irALogin) => {
    setErrorBackend('')
    try {
      await authService.registro(nombre, email, password)
      alert("¡Registro exitoso! Ya puedes iniciar sesión.")
      irALogin() // Función para cambiar la vista a Login
    } catch (error) {
      setErrorBackend(error.message)
    }
  }

  return {
    errorBackend,
    setErrorBackend,
    ejecutarLogin,
    ejecutarRegistro
  }
}