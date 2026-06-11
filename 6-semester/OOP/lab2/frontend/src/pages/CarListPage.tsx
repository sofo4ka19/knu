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

    if (loading) return <div className="loading">Завантаження автомобілів...</div>

    return (
        <div>
            <h1>Доступні автомобілі</h1>
            {cars.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">🚗</div>
                    <p>Автомобілі відсутні</p>
                </div>
            ) : (
                <div className="cars-grid">
                    {cars.map(car => (
                        <div key={car.id} className="car-card">
                            {car.imageUrl
                                ? <img src={car.imageUrl} alt={`${car.brand} ${car.model}`}
                                       onError={e => e.currentTarget.style.display = 'none'} />
                                : <div className="car-card-placeholder">🚗</div>
                            }
                            <div className="car-card-body">
                                <div className="car-card-title">{car.brand} {car.model} ({car.year})</div>
                                <div className="car-card-price">{car.pricePerDay} грн/день</div>
                                <div className={`car-card-status ${car.status === 'AVAILABLE' ? 'available' : 'unavailable'}`}>
                                    {car.status === 'AVAILABLE' ? '✓ Доступний' : '✗ Недоступний'}
                                </div>
                                <button
                                    className="btn btn-primary btn-block"
                                    onClick={() => handleRent(car.id)}
                                    disabled={car.status !== 'AVAILABLE'}
                                >
                                    {car.status === 'AVAILABLE' ? 'Орендувати' : 'Недоступно'}
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
