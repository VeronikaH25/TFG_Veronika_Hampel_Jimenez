// src/pages/Auth.jsx
import React, { useState } from 'react'
import { useAuthController } from '../controllers/useAuthController'

export default function Auth() {
  const [esLogin, setEsLogin] = useState(true)
  
  const [nombre, setNombre] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  // Nos traemos el cerebro desde el Controller
  const { errorBackend, setErrorBackend, ejecutarLogin, ejecutarRegistro } = useAuthController()

  const manejarSubmit = (e) => {
    e.preventDefault()
    if (esLogin) {
      ejecutarLogin(email, password)
    } else {
      // Le pasamos una función para que el controller pueda cambiar a la vista de login si todo va bien
      ejecutarRegistro(nombre, email, password, () => setEsLogin(true))
    }
  }

  return (
    <div className="min-h-screen w-full flex flex-col md:flex-row bg-gymDark font-['Urbanist']">
      
      <div className="hidden md:flex md:w-1/2 relative overflow-hidden bg-black">
        <img 
          src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1470&auto=format&fit=crop" 
          alt="Gym Inmersivo"
          className="absolute inset-0 w-full h-full object-cover opacity-60"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-transparent to-gymDark"></div>
        <div className="relative z-10 p-12 flex flex-col justify-end h-full">
          <h1 className="text-6xl font-['Space_Grotesk'] font-bold uppercase tracking-tighter leading-none">
            Gym <br />
            <span className="text-gymNeon drop-shadow-[0_0_15px_rgba(204,255,0,0.5)]">Vero</span>
          </h1>
          <p className="text-xl text-gray-300 mt-4 max-w-md">
            Entrena con inteligencia. Resultados optimizados por nuestra IA de alto rendimiento.
          </p>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-8">
        <div className="max-w-md w-full">
          
          <div className="mb-10 text-center md:text-left">
            <h2 className="text-4xl font-['Space_Grotesk'] font-bold mb-2">
              {esLogin ? 'BIENVENIDO' : 'ÚNETE AL GYM'}
            </h2>
            <p className="text-gray-400">
              {esLogin ? 'Introduce tus credenciales para entrenar.' : 'Crea tu cuenta en segundos.'}
            </p>
          </div>

          {errorBackend && (
            <div className="bg-red-900/50 border border-red-500 text-red-200 p-3 rounded mb-6 text-sm">
              {errorBackend}
            </div>
          )}

          <form className="space-y-6" onSubmit={manejarSubmit}>
            
            {!esLogin && (
              <div>
                <label className="block text-sm font-bold text-gray-400 mb-2">NOMBRE COMPLETO</label>
                <input 
                  type="text" 
                  value={nombre}
                  onChange={(e) => setNombre(e.target.value)}
                  className="w-full bg-gymCard border-b-2 border-gray-800 p-3 focus:border-gymNeon focus:outline-none transition-colors"
                  placeholder="Tu nombre"
                  required={!esLogin}
                />
              </div>
            )}

            <div>
              <label className="block text-sm font-bold text-gray-400 mb-2">EMAIL</label>
              <input 
                type="email" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-gymCard border-b-2 border-gray-800 p-3 focus:border-gymNeon focus:outline-none transition-colors"
                placeholder="email@ejemplo.com"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-400 mb-2">CONTRASEÑA</label>
              <input 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-gymCard border-b-2 border-gray-800 p-3 focus:border-gymNeon focus:outline-none transition-colors"
                placeholder="••••••••"
                required
              />
            </div>

            <button 
              type="submit"
              className="w-full bg-gymNeon text-black font-bold py-4 rounded-sm tracking-widest hover:bg-white transition-all shadow-[0_0_20px_rgba(204,255,0,0.3)] active:scale-95"
            >
              {esLogin ? 'INICIAR SESIÓN' : 'CREAR CUENTA'}
            </button>
          </form>

          <div className="mt-8 text-center">
            <button 
              type="button"
              onClick={() => {
                setEsLogin(!esLogin)
                setErrorBackend('')
              }}
              className="text-gray-400 text-sm hover:text-gymNeon transition-colors"
            >
              {esLogin ? '¿No tienes cuenta? Regístrate aquí' : '¿Ya eres miembro? Inicia sesión'}
            </button>
          </div>

        </div>
      </div>

    </div>
  )
}