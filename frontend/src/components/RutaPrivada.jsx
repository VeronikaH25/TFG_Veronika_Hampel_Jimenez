// src/components/RutaPrivada.jsx
import React from 'react'
import { Navigate } from 'react-router-dom'

export default function RutaPrivada({ children }) {
  // Recuperamos el JWT del almacenamiento local del navegador
  const token = localStorage.getItem('token')

  // Si el usuario no está autenticado, interceptamos la navegación y redirigimos al login
  if (!token) {
    return <Navigate to="/" replace />
  }

  // Si la sesión es válida, renderizamos el componente hijo solicitado
  return children
}