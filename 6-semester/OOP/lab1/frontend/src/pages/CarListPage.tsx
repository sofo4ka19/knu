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
                        {car.imageUrl && <img src={car.imageUrl} alt={car.brand} />}
                        <h3>{car.brand} {car.model} ({car.year})</h3>
                        <p><strong>{car.pricePerDay} грн/день</strong></p>
                        <button onClick={() => handleRent(car.id)}>
                            {isAuthenticated ? 'Орендувати' : 'Увійти та орендувати'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}