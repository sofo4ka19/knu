import { Routes, Route } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'
import Navbar from './components/Navbar'
import CarListPage from './pages/CarListPage'
import OrderFormPage from './pages/OrderFormPage'
import MyOrdersPage from './pages/MyOrdersPage'
import AdminDashboard from './pages/admin/AdminDashboard'
import ProtectedRoute from './components/ProtectedRoute'

export default function App() {
  const { isLoading } = useAuth0()
  if (isLoading) return <div className="loading">Завантаження...</div>

  return (
      <>
        <Navbar />
        <main className="container">
          <Routes>
            <Route path="/"           element={<CarListPage />} />
            <Route path="/order/:id"  element={
              <ProtectedRoute><OrderFormPage /></ProtectedRoute>
            } />
            <Route path="/my-orders"  element={
              <ProtectedRoute><MyOrdersPage /></ProtectedRoute>
            } />
            <Route path="/admin"      element={
              <ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>
            } />
          </Routes>
        </main>
      </>
  )
}