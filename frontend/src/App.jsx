// src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Auth from './pages/Auth.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Perfil from './pages/Perfil.jsx' 
import GenerarRutina from './pages/GenerarRutina'
import RutaPrivada from './components/RutaPrivada.jsx'
import GenerarFase2 from './pages/GenerarFase2'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Ruta pública (cualquiera puede entrar) */}
        <Route path="/" element={<Auth />} />
        
        {/* Rutas protegidas (solo los que tienen Token) */}
        <Route 
          path="/dashboard" 
          element={
            <RutaPrivada>
              <Dashboard />
            </RutaPrivada>
          } 
        />
        
        <Route 
          path="/perfil" 
          element={
            <RutaPrivada>
              <Perfil />
            </RutaPrivada>
          } 
        />
        
        {/* FASE 2: Vista del selector dinámico (Bandit) */}
        <Route 
          path="/generar-fase-2" 
          element={
            <RutaPrivada>
              <GenerarFase2 />
            </RutaPrivada>
          }
        />

        {/* FASE 1: Vista de experimentación ciega (A/B Testing)  */}
        <Route 
          path="/generar-rutina" 
          element={
            <RutaPrivada>
              <GenerarRutina />
            </RutaPrivada>
          } 
        />

      </Routes>
    </BrowserRouter>
  )
}

export default App