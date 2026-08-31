// src/pages/Perfil.jsx
import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import userService from '../services/userService'

export default function Perfil() {
  const navigate = useNavigate()
  
  // 1. Añadimos diasEntreno al estado inicial (por defecto 3)
  const [datos, setDatos] = useState({ 
    peso: '', 
    edad: '', 
    objetivo: 'Fuerza',
    nivel: 'Principiante',
    diasEntreno: '3'
  })
  
  const [guardando, setGuardando] = useState(false)

  // 2. Recuperamos los datos de Mongo
  useEffect(() => {
    userService.obtenerPerfil().then(res => {
      setDatos({
        peso: res.peso || '',
        edad: res.edad || '',
        objetivo: res.objetivo || 'Fuerza',
        nivel: res.nivel || 'Principiante',
        diasEntreno: res.dias_entreno || '3' // Ojo a cómo se llame en tu BD
      })
    })
  }, [])

  const handleChangeNumerico = (e) => {
    const { name, value } = e.target
    const soloNumeros = value.replace(/\D/g, '')
    setDatos({ ...datos, [name]: soloNumeros })
  }

  const handleChangeSelect = (e) => {
    const { name, value } = e.target
    setDatos({ ...datos, [name]: value })
  }

  // 3. Función para destruir el token y salir
  const handleCerrarSesion = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('nombre')
    navigate('/')
  }

  // 4. Guardar datos en el backend
  const manejarGuardar = async () => {
    if (!datos.peso || !datos.edad) {
      alert("Por favor, rellena tu peso y edad.")
      return
    }

    setGuardando(true)
    try {
      const payload = {
        peso: parseFloat(datos.peso),
        edad: parseInt(datos.edad),
        objetivo: datos.objetivo,
        nivel: datos.nivel,
        dias_entreno: parseInt(datos.diasEntreno) // Pasamos los días como entero
      }

      await userService.actualizarPerfil(payload)
      alert("¡Perfil actualizado con éxito! La IA ya está lista.")
      navigate('/dashboard') 
    } catch (error) {
      alert("Error al guardar los datos. ¿Está el backend encendido?")
    } finally {
      setGuardando(false)
    }
  }

  return (
    <div className="min-h-screen bg-gymDark text-white p-8 font-['Urbanist']">
      <div className="max-w-xl mx-auto">
        
        {/* NAVEGACIÓN SUPERIOR */}
        <div className="flex justify-between items-center mb-8">
          <Link to="/dashboard" className="text-gymNeon text-sm hover:underline tracking-widest">
            ← VOLVER AL PANEL
          </Link>
          <button 
            onClick={handleCerrarSesion}
            className="text-red-500 text-sm hover:text-red-400 transition-colors tracking-widest font-bold"
          >
            CERRAR SESIÓN
          </button>
        </div>
        
        <h2 className="text-4xl font-['Space_Grotesk'] font-bold mb-2 uppercase">Configuración Física</h2>
        <p className="text-gray-400 mb-10 text-sm">Estos datos son imprescindibles para el cálculo de la IA.</p>

        <form className="space-y-8 bg-gymCard p-8 rounded-sm border border-gray-800">
           
           <div className="space-y-6">
              {/* FILA 1: Peso y Edad */}
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-bold text-gray-500 tracking-widest mb-2">PESO ACTUAL (KG)</label>
                  <input 
                    name="peso"
                    value={datos.peso} 
                    onChange={handleChangeNumerico}
                    type="text" 
                    inputMode="numeric"
                    maxLength="3"
                    className="w-full bg-black border-b border-gray-700 p-3 focus:border-gymNeon focus:outline-none transition-colors" 
                    placeholder="Ej: 75"
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-gray-500 tracking-widest mb-2">EDAD</label>
                  <input 
                    name="edad"
                    value={datos.edad} 
                    onChange={handleChangeNumerico}
                    type="text" 
                    inputMode="numeric"
                    maxLength="2"
                    className="w-full bg-black border-b border-gray-700 p-3 focus:border-gymNeon focus:outline-none transition-colors" 
                    placeholder="Ej: 24"
                  />
                </div>
              </div>

              {/* FILA 2: Objetivo y Nivel */}
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <label className="block text-xs font-bold text-gray-500 tracking-widest mb-2">OBJETIVO</label>
                  <select 
                    name="objetivo"
                    value={datos.objetivo}
                    onChange={handleChangeSelect}
                    className="w-full bg-black border-b border-gray-700 p-3 focus:border-gymNeon focus:outline-none text-white cursor-pointer"
                  >
                    <option value="Fuerza">Fuerza</option>
                    <option value="Hipertrofia">Hipertrofia</option>
                    <option value="Definición">Definición</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-500 tracking-widest mb-2">NIVEL</label>
                  <select 
                    name="nivel"
                    value={datos.nivel}
                    onChange={handleChangeSelect}
                    className="w-full bg-black border-b border-gray-700 p-3 focus:border-gymNeon focus:outline-none text-white cursor-pointer"
                  >
                    <option value="Principiante">Principiante</option>
                    <option value="Intermedio">Intermedio</option>
                    <option value="Avanzado">Avanzado</option>
                  </select>
                </div>
              </div>

              {/* FILA 3: Días de Entrenamiento */}
              <div>
                <label className="block text-xs font-bold text-gray-500 tracking-widest mb-2">DÍAS DE ENTRENO (SEMANALES)</label>
                <select 
                  name="diasEntreno"
                  value={datos.diasEntreno}
                  onChange={handleChangeSelect}
                  className="w-full bg-black border-b border-gray-700 p-3 focus:border-gymNeon focus:outline-none text-white cursor-pointer"
                >
                  <option value="3">3 Días</option>
                  <option value="4">4 Días</option>
                  <option value="5">5 Días</option>
                </select>
              </div>

           </div>
           
           <button 
             type="button" 
             onClick={manejarGuardar}
             disabled={guardando}
             className="w-full bg-white text-black font-bold py-4 hover:bg-gymNeon transition-all tracking-widest disabled:opacity-50 mt-4"
           >
             {guardando ? 'GUARDANDO...' : 'GUARDAR CAMBIOS'}
           </button>

        </form>
      </div>
    </div>
  )
}