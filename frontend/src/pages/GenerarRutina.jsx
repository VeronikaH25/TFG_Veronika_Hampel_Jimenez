import React, { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import rutinaService from '../services/rutinaService'
import userService from '../services/userService'

export default function GenerarRutina() {
  const navigate = useNavigate()
  const [cargando, setCargando] = useState(true)
  const [rutinasOpciones, setRutinasOpciones] = useState(null)
  const [error, setError] = useState('')
  
  const [puntuacionA, setPuntuacionA] = useState(3)
  const [puntuacionB, setPuntuacionB] = useState(3)

  useEffect(() => {
    const cargarDatos = async () => {
      try {
        const opciones = await rutinaService.generarRutinas()
        setRutinasOpciones(opciones)
      } catch (err) {
        setError(err.message)
      } finally {
        setCargando(false)
      }
    }
    cargarDatos()
  }, [])

  const manejarVoto = async (opcionElegida, nombreOpcion) => {
    try {
      // Enviamos un paquete completo con los datos de ambos modelos
      await rutinaService.votarRutina({
        origen_elegido: opcionElegida.origen,
        rutina_json: opcionElegida.rutina,
        origen_opcion_1: rutinasOpciones.opcion_1.origen,
        puntuacion_opcion_1: parseInt(puntuacionA),
        origen_opcion_2: rutinasOpciones.opcion_2.origen,
        puntuacion_opcion_2: parseInt(puntuacionB)
      })
      alert(`¡Votos registrados! Has activado la ${nombreOpcion}.`)
      navigate('/dashboard') 
    } catch (error) {
      alert("Error al guardar las votaciones.")
    }
  }

  const RenderRutina = ({ rutina }) => {
    const datosEntreno = rutina.rutina ? rutina.rutina : rutina;

    return (
      <div className="text-left text-sm text-gray-300 space-y-4 max-h-80 overflow-y-auto pr-2 custom-scrollbar">
        {Object.entries(datosEntreno).map(([dia, ejercicios]) => {
          if (!dia.startsWith('dia')) return null;

          return (
            <div key={dia} className="border-b border-gray-800 pb-2 last:border-0">
              <h4 className="text-gymNeon font-bold uppercase mb-2 text-xs tracking-tighter">{dia.replace('_', ' ')}</h4>
              <ul className="space-y-1">
                {Array.isArray(ejercicios) && ejercicios.map((ej, idx) => (
                  <li key={idx} className="flex justify-between border-l-2 border-gray-700 pl-2 hover:bg-white/5 transition-colors">
                    <span className="truncate pr-2">{ej.ejercicio}</span>
                    <span className="text-gray-500 font-mono shrink-0">{ej.series}x{ej.reps}</span>
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
      <div className="max-w-6xl mx-auto">
        
        <div className="mb-10 text-center">
          <Link to="/dashboard" className="text-gymNeon text-xs tracking-[0.2em] hover:underline uppercase">
            ← Cancelar y volver
          </Link>
        </div>

        {cargando && (
          <div className="flex flex-col items-center justify-center py-20 animate-pulse">
            <div className="w-12 h-12 border-2 border-gymNeon border-t-transparent rounded-full animate-spin mb-6"></div>
            <h3 className="text-xl font-['Space_Grotesk'] font-bold text-gymNeon uppercase tracking-widest">
              Consultando al Orquestador Híbrido...
            </h3>
            <p className="text-gray-500 mt-2">Esto puede tardar unos segundos mientras la IA procesa los modelos.</p>
          </div>
        )}

        {error && (
          <div className="max-w-md mx-auto bg-red-900/20 border border-red-500/50 p-6 text-center">
            <p className="text-red-200 mb-4">{error}</p>
            <button onClick={() => navigate('/perfil')} className="bg-white text-black px-6 py-2 font-bold text-xs">IR AL PERFIL</button>
          </div>
        )}

        {!cargando && rutinasOpciones && (
          <div className="animate-fade-in">
            <div className="text-center mb-12">
              <h2 className="text-4xl font-['Space_Grotesk'] font-bold uppercase mb-2 italic">Selección de Algoritmo</h2>
              <p className="text-gray-400">Compara estas dos propuestas. No sabrás cuál es IA o KNN hasta que elijas.</p>
            </div>

            <div className="grid md:grid-cols-2 gap-10">
              {/* OPCIÓN A */}
              <div className="bg-gymCard border border-gray-800 p-8 rounded-sm hover:border-gymNeon/30 transition-all">
                <h3 className="text-xl font-bold font-['Space_Grotesk'] mb-6 tracking-widest">OPCIÓN A</h3>
                <div className="bg-black/50 p-5 rounded-sm border border-gray-900 mb-8">
                  <RenderRutina rutina={rutinasOpciones.opcion_1.rutina} />
                </div>
                <div className="mb-8">
                  <p className="text-[10px] font-bold text-gray-500 tracking-widest mb-4 uppercase text-center">Calidad percibida ({puntuacionA}/5)</p>
                  <input type="range" min="1" max="5" value={puntuacionA} onChange={(e) => setPuntuacionA(e.target.value)} className="w-full accent-gymNeon" />
                </div>
                <button onClick={() => manejarVoto(rutinasOpciones.opcion_1, 'Opción A')} className="w-full bg-white text-black font-bold py-4 hover:bg-gymNeon transition-all tracking-widest uppercase text-sm">
                  Activar Opción A
                </button>
              </div>

              {/* OPCIÓN B */}
              <div className="bg-gymCard border border-gray-800 p-8 rounded-sm hover:border-gymNeon/30 transition-all">
                <h3 className="text-xl font-bold font-['Space_Grotesk'] mb-6 tracking-widest">OPCIÓN B</h3>
                <div className="bg-black/50 p-5 rounded-sm border border-gray-900 mb-8">
                  <RenderRutina rutina={rutinasOpciones.opcion_2.rutina} />
                </div>
                <div className="mb-8">
                  <p className="text-[10px] font-bold text-gray-500 tracking-widest mb-4 uppercase text-center">Calidad percibida ({puntuacionB}/5)</p>
                  <input type="range" min="1" max="5" value={puntuacionB} onChange={(e) => setPuntuacionB(e.target.value)} className="w-full accent-gymNeon" />
                </div>
                <button onClick={() => manejarVoto(rutinasOpciones.opcion_2, 'Opción B')} className="w-full bg-white text-black font-bold py-4 hover:bg-gymNeon transition-all tracking-widest uppercase text-sm">
                  Activar Opción B
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}