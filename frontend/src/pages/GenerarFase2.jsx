import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import rutinaService from '../services/rutinaService'
import userService from '../services/userService'

export default function GenerarFase2() {
  const navigate = useNavigate()
  const [cargando, setCargando] = useState(true)
  const [resultado, setResultado] = useState(null)
  const [error, setError] = useState('')
  const [puntuacion, setPuntuacion] = useState(3) // Estado para el voto
  const [usuarioEmail, setUsuarioEmail] = useState('')

  // --- NUEVO: Textos dinámicos de carga ---
  const mensajesCarga = [
    "El Orquestador está decidiendo...",
    "Calculando distancias matemáticas k-NN...",
    "Consultando al Agente IA...",
    "Validando biomecánica de los ejercicios...",
    "Ajustando series y repeticiones...",
    "Empaquetando tu rutina óptima..."
  ]
  const [indiceMensaje, setIndiceMensaje] = useState(0)

  useEffect(() => {
    let intervalo
    if (cargando) {
      intervalo = setInterval(() => {
        setIndiceMensaje((prev) => (prev + 1) % mensajesCarga.length)
      }, 2500) // Cambia el texto cada 2.5 segundos
    }
    return () => clearInterval(intervalo)
  }, [cargando])
  // ----------------------------------------

  useEffect(() => {
    const cargarRutinaInteligente = async () => {
      try {
        const perfilUsuario = await userService.obtenerPerfil()
        if (!perfilUsuario || !perfilUsuario.peso || !perfilUsuario.objetivo) {
          throw new Error("Debes completar tu perfil físico antes de generar una rutina.")
        }
        setUsuarioEmail(perfilUsuario.email)

        const data = await rutinaService.generarRutinaFase2(perfilUsuario)
        setResultado(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setCargando(false)
      }
    }
    cargarRutinaInteligente()
  }, [])

  // Nueva función que VOTA y GUARDA
  const guardarYVotarActiva = async () => {
    try {
      await rutinaService.votarFase2({
        email_usuario: usuarioEmail,
        algoritmo_utilizado: resultado.algoritmo_utilizado,
        puntuacion: parseInt(puntuacion),
        rutina_json: resultado.rutina
      })
      // Redirección directa e instantánea sin ventanitas molestas
      navigate('/dashboard')
    } catch (err) {
      console.error("Fallo al guardar:", err)
      alert(`⚠️ Ups: ${err.message}`) 
    }
  }

  const RenderRutina = ({ rutina }) => {
    const datosEntreno = rutina.rutina ? rutina.rutina : rutina;
    return (
      <div className="text-left text-sm text-gray-300 space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
        {Object.entries(datosEntreno).map(([dia, ejercicios]) => {
          if (!dia.startsWith('dia')) return null;
          return (
            <div key={dia} className="border-b border-gray-800 pb-4 last:border-0">
              <h4 className="text-gymNeon font-bold uppercase mb-3 text-sm tracking-tighter">{dia.replace('_', ' ')}</h4>
              <ul className="space-y-2">
                {Array.isArray(ejercicios) && ejercicios.map((ej, idx) => (
                  <li key={idx} className="flex justify-between border-l-2 border-gymNeon/50 pl-3 hover:bg-white/5 p-2 rounded transition-colors">
                    <span className="font-semibold text-white">{ej.ejercicio}</span>
                    <span className="text-gymNeon font-mono shrink-0 ml-4">{ej.series}x{ej.reps}</span>
                  </li>
                ))}
              </ul>
            </div>
          )
        })}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gymDark text-white font-['Urbanist'] p-6">
      <div className="max-w-3xl mx-auto">
        <div className="mb-10 text-center">
          <Link to="/dashboard" className="text-gymNeon text-xs tracking-[0.2em] hover:underline uppercase">
            ← Cancelar y volver
          </Link>
        </div>

        {cargando && (
          <div className="flex flex-col items-center justify-center py-20 animate-pulse">
            <div className="w-16 h-16 border-4 border-gymNeon border-t-transparent rounded-full animate-spin mb-8"></div>
            {/* TEXTO DINÁMICO IMPLEMENTADO AQUÍ */}
            <h3 className="text-xl font-['Space_Grotesk'] font-bold text-gymNeon uppercase tracking-widest text-center transition-opacity duration-500">
              {mensajesCarga[indiceMensaje]}
            </h3>
          </div>
        )}

        {error && (
          <div className="max-w-md mx-auto bg-red-900/20 border border-red-500/50 p-6 text-center">
            <p className="text-red-200 mb-4">{error}</p>
            <button onClick={() => navigate('/perfil')} className="bg-white text-black px-6 py-2 font-bold text-xs">
              IR AL PERFIL
            </button>
          </div>
        )}

        {!cargando && resultado && !error && (
          <div className="animate-fade-in bg-gymCard border border-gray-800 p-8 rounded-sm shadow-2xl">
            <div className="text-center mb-6 border-b border-gray-800 pb-6">
              <h2 className="text-3xl font-['Space_Grotesk'] font-bold uppercase mb-4 italic">Tu Rutina Óptima</h2>
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-black rounded-full border border-gray-700">
                <span className="w-2 h-2 rounded-full bg-gymNeon animate-pulse"></span>
                <span className="text-[10px] text-gray-400 tracking-[0.2em] uppercase">
                  Modelo: <span className="text-white font-bold">{resultado.algoritmo_utilizado.toUpperCase()}</span> 
                </span>
              </div>
            </div>

            <div className="bg-black/50 p-6 rounded-sm border border-gray-900 mb-8">
              <RenderRutina rutina={resultado.rutina} />
            </div>

            {/* SECCIÓN DE VOTACIÓN AÑADIDA */}
            <div className="bg-black/30 p-6 border border-gray-800 rounded-sm mb-6 text-center">
              <h3 className="text-sm font-bold text-gray-400 tracking-widest mb-4 uppercase">¿Qué te parece esta rutina?</h3>
              <p className="text-[10px] text-gray-500 mb-4 uppercase">Tu nota ayuda a la IA a mejorar (Nota: {puntuacion}/5)</p>
              <input 
                type="range" 
                min="1" 
                max="5" 
                value={puntuacion} 
                onChange={(e) => setPuntuacion(e.target.value)} 
                className="w-full max-w-sm mx-auto accent-gymNeon" 
              />
            </div>

            <button 
              onClick={guardarYVotarActiva} 
              className="w-full bg-gymNeon text-black font-bold py-4 hover:bg-white transition-all tracking-widest uppercase text-sm"
            >
              Guardar y Empezar a Entrenar
            </button>
          </div>
        )}
      </div>
    </div>
  )
}