import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'
import { createAuthApi, publicApi } from '../api/apiClient'
import type { Car } from '../types'

export default function OrderFormPage() {
    const { id } = useParams<{ id: string }>()
    const navigate = useNavigate()
    const { getAccessTokenSilently } = useAuth0()

    const [car, setCar] = useState<Car | null>(null)
    const [form, setForm] = useState({
        passportData: '',
        startDate: '',
        endDate: '',
    })
    const [error, setError] = useState('')
    const [totalPrice, setTotalPrice] = useState<number | null>(null)

    useEffect(() => {
        publicApi.get<Car>(`/cars/${id}`).then(res => setCar(res.data))
    }, [id])

    // Розраховуємо ціну на льоту при зміні дат
    useEffect(() => {
        if (car && form.startDate && form.endDate) {
            const days = Math.ceil(
                (new Date(form.endDate).getTime() - new Date(form.startDate).getTime())
                / (1000 * 60 * 60 * 24)
            )
            if (days > 0) setTotalPrice(days * car.pricePerDay)
            else setTotalPrice(null)
        }
    }, [form.startDate, form.endDate, car])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')
        try {
            const api = createAuthApi(() => getAccessTokenSilently())
            await api.post('/orders', { carId: Number(id), ...form })
            navigate('/my-orders')
        } catch (err: any) {
            setError(err.message)
        }
    }

    if (!car) return <div>Завантаження...</div>

    return (
        <div className="order-form">
            <h2>Оренда: {car.brand} {car.model}</h2>
            <p>Ціна: {car.pricePerDay} грн/день</p>

            {error && <div className="error">{error}</div>}

            <form onSubmit={handleSubmit}>
                <input placeholder="Паспортні дані (серія та номер)"
                       value={form.passportData}
                       onChange={e => setForm({...form, passportData: e.target.value})}
                       required />
                <label>Дата початку
                    <input type="date" value={form.startDate}
                           min={new Date().toISOString().split('T')[0]}
                           onChange={e => setForm({...form, startDate: e.target.value})}
                           required />
                </label>
                <label>Дата закінчення
                    <input type="date" value={form.endDate}
                           min={form.startDate}
                           onChange={e => setForm({...form, endDate: e.target.value})}
                           required />
                </label>

                {totalPrice && (
                    <p className="total">Разом: <strong>{totalPrice} грн</strong></p>
                )}

                <button type="submit">Підтвердити замовлення</button>
            </form>
        </div>
    )
}