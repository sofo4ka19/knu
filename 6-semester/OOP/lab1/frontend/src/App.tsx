import { Routes, Route, useNavigate, Navigate } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'
import { useEffect } from 'react'
import Navbar from './components/Navbar'
import CarListPage from './pages/CarListPage'
import OrderFormPage from './pages/OrderFormPage'
import MyOrdersPage from './pages/MyOrdersPage'
import AdminDashboard from './pages/admin/AdminDashboard'
import ProtectedRoute from './components/ProtectedRoute'

export default function App() {
    const { isLoading, isAuthenticated, user } = useAuth0()
    const navigate = useNavigate()

    const isAdmin = isAuthenticated &&
        ((user?.['https://car-rental-api/roles'] as string[]) ?? []).includes('admin')

    useEffect(() => {
        if (isAuthenticated) {
            const returnTo = sessionStorage.getItem('returnTo')
            if (returnTo) {
                sessionStorage.removeItem('returnTo')
                navigate(returnTo)
            }
        }
    }, [isAuthenticated])

    return (
        <>
            <Navbar />
            <main className="container">
                <Routes>
                    <Route path="/" element={
                        isAdmin ? <Navigate to="/admin" replace /> : <CarListPage />
                    } />
                    <Route path="/order/:id" element={
                        isAdmin ? <Navigate to="/admin" replace /> :
                        <ProtectedRoute><OrderFormPage /></ProtectedRoute>
                    } />
                    <Route path="/my-orders" element={
                        isAdmin ? <Navigate to="/admin" replace /> :
                        <ProtectedRoute><MyOrdersPage /></ProtectedRoute>
                    } />
                    <Route path="/admin" element={
                        <ProtectedRoute adminOnly><AdminDashboard /></ProtectedRoute>
                    } />
                </Routes>
            </main>
        </>
    )
}