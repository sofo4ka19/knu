import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'
import { publicApi } from '../api/apiClient'
import type { Car } from '../types'

export default function CarListPage() {
    const [cars, setCars] = useState<Car[]>([])
    const [loading, setLoading] = useState(true)
    const { isAuthenticated, loginWithRedirect } = useAuth0()
    const navigate = useNavigate()

    useEffect(() => {
        publicApi.get<Car[]>('/cars')
            .then(res => setCars(res.data))
            .finally(() => setLoading(false))
    }, [])

    const handleRent = (carId: number) => {
        if (!isAuthenticated) loginWithRedirect()
        else navigate(`/order/${carId}`)
    }

    if (loading) return <div>Завантаження авто...</div>

    return (
        <div>
            <h1>Доступні автомобілі</h1>
            <div className="cars-grid">
                {cars.map(car => (
                    <div key={car.id} className="car-card">
                        {car.imageUrl ? (
                            <img src={car.imageUrl} alt={car.brand}
                                 onError={(e) => e.currentTarget.style.display = 'none'}
                                 style={{width: '100%', height: '200px', objectFit: 'cover'}}
                            />
                        ) : (
                            <div style={{
                                width: '100%', height: '200px',
                                backgroundColor: '#e2e8f0',
                                display: 'flex', alignItems: 'center',
                                justifyContent: 'center', fontSize: '48px'
                            }}>🚗</div>
                        )}
                        <h3>{car.brand} {car.model} ({car.year})</h3>
                        <p><strong>{car.pricePerDay} грн/день</strong></p>

                        {/* Показуємо статус */}
                        <p style={{
                            color: car.status === 'AVAILABLE' ? 'green' : 'red',
                            fontWeight: 'bold'
                        }}>
                            {car.status === 'AVAILABLE' ? '✅ Доступний' : '🔧 Недоступний'}
                        </p>

                        <button
                            onClick={() => handleRent(car.id)}
                            disabled={car.status !== 'AVAILABLE'}
                            style={{
                                opacity: car.status !== 'AVAILABLE' ? 0.5 : 1,
                                cursor: car.status !== 'AVAILABLE' ? 'not-allowed' : 'pointer'
                            }}
                        >
                            {car.status === 'AVAILABLE' ? 'Орендувати' : 'Недоступно'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}