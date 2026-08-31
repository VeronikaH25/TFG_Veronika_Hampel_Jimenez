import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import userService from '../services/userService'

export default function Dashboard() {
  const navigate = useNavigate()
  const [usuario, setUsuario] = useState(null)
  const [errorIA, setErrorIA] = useState('')

  useEffect(() => {
    userService.obtenerPerfil()
      .then(setUsuario)
      .catch(() => navigate('/'))
  }, [navigate])

  // Validamos antes de ir a la Fase 1
  const irAFase1 = () => {
    if (!usuario?.peso || !usuario?.edad || !usuario?.objetivo || !usuario?.dias_entreno) {
      setErrorIA('⚠️ ERROR: Necesitamos tus datos físicos para que el sistema sea preciso. Ve a tu Perfil.')
      return
    }
    navigate('/generar-rutina')
  }

  // Validamos antes de ir a la Fase 2 (Bandit)
  const irAFase2 = () => {
    if (!usuario?.peso || !usuario?.edad || !usuario?.objetivo || !usuario?.dias_entreno) {
      setErrorIA('⚠️ ERROR: Necesitamos tus datos físicos para que el sistema sea preciso. Ve a tu Perfil.')
      return
    }
    navigate('/generar-fase-2')
  }

  // Componente para renderizar la rutina guardada
  const VistaRutinaActiva = ({ rutina }) => {
    const datos = rutina.rutina ? rutina.rutina : rutina;
    
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl mt-8 animate-fade-in">
        {Object.entries(datos).map(([dia, ejercicios]) => (
          <div key={dia} className="bg-gymCard border border-gray-800 p-6 rounded-sm">
            <h3 className="text-gymNeon font-['Space_Grotesk'] font-bold uppercase mb-4 border-b border-gray-800 pb-2 text-sm tracking-widest">
              {dia.replace('_', ' ')}
            </h3>
            <ul className="space-y-3">
              {Array.isArray(ejercicios) && ejercicios.map((ej, idx) => (
                <li key={idx} className="flex justify-between items-start group">
                  <span className="text-gray-300 text-sm group-hover:text-white transition-colors">{ej.ejercicio}</span>
                  <span className="text-gymNeon font-mono text-xs bg-gymNeon/10 px-2 py-1 rounded-sm ml-4">
                    {ej.series}x{ej.reps}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    )
  }

  // Subcomponente de los botones para no repetir código
  const BotonesGeneracion = () => (
    <div className="mt-8 grid md:grid-cols-2 gap-6 w-full max-w-4xl animate-fade-in">
      {/* BOTÓN FASE 1: A/B Testing */}
      <div className="bg-gymCard border border-gray-800 p-6 rounded-sm text-center hover:border-gray-500 transition-all flex flex-col justify-between">
        <div>
          <h3 className="text-xl font-bold font-['Space_Grotesk'] mb-2 text-white">Fase 1: Entrenamiento</h3>
          <p className="text-gray-400 text-sm mb-6">
            Ayuda a nuestra IA a mejorar. Compara dos rutinas generadas por distintos algoritmos y vota la mejor.
          </p>
        </div>
        <button 
          onClick={irAFase1}
          className="block w-full bg-transparent border border-white text-white font-bold py-3 hover:bg-white hover:text-black transition-all tracking-widest uppercase text-xs"
        >
          Evaluar Algoritmos
        </button>
      </div>

      {/* BOTÓN FASE 2: Bandit Inteligente */}
      <div className="bg-gymCard border border-gymNeon/30 p-6 rounded-sm text-center relative overflow-hidden flex flex-col justify-between">
        <div className="absolute top-0 right-0 bg-gymNeon text-black text-[9px] font-bold px-2 py-1 uppercase tracking-widest">
          Recomendado
        </div>
        <div>
          <h3 className="text-xl font-bold font-['Space_Grotesk'] mb-2 text-gymNeon">Fase 2: Modo Inteligente</h3>
          <p className="text-gray-400 text-sm mb-6">
            Obtén tu rutina óptima. El sistema elegirá automáticamente el mejor modelo basándose en el histórico.
          </p>
        </div>
        <button 
          onClick={irAFase2}
          className="block w-full bg-gymNeon text-black font-bold py-3 hover:bg-white transition-all tracking-widest uppercase text-xs shadow-[0_0_15px_rgba(208,255,0,0.3)]"
        >
          Generar Rutina Óptima
        </button>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-gymDark text-white font-['Urbanist'] flex flex-col">
      {/* HEADER */}
      <header className="p-6 flex justify-between items-center max-w-7xl w-full mx-auto">
        <h1 className="text-2xl font-['Space_Grotesk'] font-bold tracking-tighter">
          GYM <span className="text-gymNeon">Vero</span>
        </h1>
        <Link to="/perfil" className="flex items-center gap-3 group">
          <span className="text-sm font-bold text-gray-400 group-hover:text-gymNeon transition-colors uppercase">
            {usuario?.nombre || 'Perfil'}
          </span>
          <div className="w-10 h-10 rounded-full bg-gymCard border border-gray-700 flex items-center justify-center group-hover:border-gymNeon transition-all">
             <span className="text-gymNeon text-lg">👤</span>
          </div>
        </Link>
      </header>

      <main className="flex-1 flex flex-col items-center p-6 pb-20">
        
        {/* TITULAR DINÁMICO */}
        <div className="text-center mb-6 mt-10">
          <h2 className="text-5xl font-['Space_Grotesk'] font-bold mb-4 leading-none uppercase">
            {usuario?.rutina_activa ? 'Tu Plan de' : 'Tu Próximo'} <br /> 
            <span className="text-gymNeon italic">{usuario?.rutina_activa ? 'Entrenamiento' : 'Límite'}</span>
          </h2>
          {!usuario?.rutina_activa && (
            <p className="text-gray-400 text-lg max-w-xl mx-auto">
              Selecciona cómo quieres generar tu rutina de hoy.
            </p>
          )}
        </div>

        {errorIA && (
          <div className="mb-8 p-4 bg-red-900/20 border border-red-500/50 text-red-200 rounded-sm text-sm">
            {errorIA}
          </div>
        )}

        {/* LÓGICA DE VISTA */}
        {usuario?.rutina_activa ? (
          <>
            <VistaRutinaActiva rutina={usuario.rutina_activa} />
            
            <div className="mt-16 w-full max-w-4xl border-t border-gray-800 pt-8 text-center">
              <h3 className="text-gray-400 tracking-[0.3em] uppercase text-xs font-bold mb-6">¿Quieres cambiar de rutina?</h3>
              <BotonesGeneracion />
            </div>
          </>
        ) : (
          <BotonesGeneracion />
        )}
      </main>
    </div>
  )
}