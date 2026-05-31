import { useAuth0 } from '@auth0/auth0-react'
import { Navigate } from 'react-router-dom'

interface Props {
    children: React.ReactNode
    adminOnly?: boolean
}

export default function ProtectedRoute({ children, adminOnly }: Props) {
    const { isAuthenticated, isLoading, user } = useAuth0()

    if (isLoading) return <div>Завантаження...</div>
    if (!isAuthenticated) return <Navigate to="/" replace />

    if (adminOnly) {
        const roles = (user?.['https://car-rental-api/roles'] as string[]) ?? []
        if (!roles.includes('admin')) return <Navigate to="/" replace />
    }

    return <>{children}</>
}