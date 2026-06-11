import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'
import { createAuthApi, publicApi } from '../api/apiClient'
import type { Car } from '../types'

export default function OrderFormPage() {
    const { id } = useParams<{ id: string }>()
    const navigate = useNavigate()
    const { getAccessTokenSilently, loginWithRedirect } = useAuth0()

    const [car, setCar] = useState<Car | null>(null)
    const [form, setForm] = useState({ passportData: '', startDate: '', endDate: '' })
    const [error, setError] = useState('')
    const [totalPrice, setTotalPrice] = useState<number | null>(null)

    useEffect(() => {
        publicApi.get<Car>(`/cars/${id}`).then(res => setCar(res.data))
    }, [id])

    useEffect(() => {
        const saved = sessionStorage.getItem(`orderForm_${id}`)
        if (saved) {
            sessionStorage.removeItem(`orderForm_${id}`)
            setForm(JSON.parse(saved))
        }
    }, [id])

    useEffect(() => {
        if (car && form.startDate && form.endDate) {
            const days = Math.ceil(
                (new Date(form.endDate).getTime() - new Date(form.startDate).getTime())
                / (1000 * 60 * 60 * 24)
            ) + 1
            setTotalPrice(days > 0 ? days * car.pricePerDay : null)
        }
    }, [form.startDate, form.endDate, car])

    const PASSPORT_RE = /^([А-ЯІЇЄ]{2}\d{6}|[A-Z]{2}\d{6}|\d{9})$/

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError('')

        if (!PASSPORT_RE.test(form.passportData.trim().toUpperCase())) {
            setError('Невірний формат паспорта. Приклади: АБ123456 · FF123456 · 123456789')
            return
        }

        if (form.endDate < form.startDate) {
            setError('Дата закінчення не може бути раніше дати початку')
            return
        }

        try {
            let token: string
            try {
                token = await getAccessTokenSilently()
            } catch (tokenError: any) {
                if (tokenError.error === 'consent_required' || tokenError.message === 'Consent required') {
                    sessionStorage.setItem('returnTo', `/order/${id}`)
                    sessionStorage.setItem(`orderForm_${id}`, JSON.stringify(form))
                    await loginWithRedirect({ authorizationParams: { prompt: 'consent' } })
                    return
                }
                throw tokenError
            }

            const api = createAuthApi(() => Promise.resolve(token))
            await api.post('/orders', {
                carId: Number(id),
                ...form,
                passportData: form.passportData.trim().toUpperCase(),
            })
            navigate('/my-orders')
        } catch (err: any) {
            setError(err.message)
        }
    }

    if (!car) return <div className="loading">Завантаження...</div>

    return (
        <div className="order-form-wrap">
            <div className="order-form">
                <h2>Оренда автомобіля</h2>
                <p className="order-form-subtitle">{car.brand} {car.model} · {car.pricePerDay} грн/день</p>

                {error && <div className="error">{error}</div>}

                <form onSubmit={handleSubmit}>
                    <label>
                        Паспортні дані
                        <input
                            placeholder="АБ123456 · FF123456 · 123456789"
                            value={form.passportData}
                            onChange={e => setForm({ ...form, passportData: e.target.value })}
                            required
                        />
                    </label>

                    <label>
                        Дата початку
                        <input type="date" value={form.startDate}
                               min={new Date().toISOString().split('T')[0]}
                               onChange={e => {
                                   const newStart = e.target.value
                                   setForm(prev => ({
                                       ...prev,
                                       startDate: newStart,
                                       endDate: prev.endDate && prev.endDate < newStart ? newStart : prev.endDate,
                                   }))
                               }}
                               required />
                    </label>

                    <label>
                        Дата закінчення
                        <input type="date" value={form.endDate}
                               min={form.startDate || new Date().toISOString().split('T')[0]}
                               onChange={e => setForm({ ...form, endDate: e.target.value })}
                               required />
                    </label>

                    {totalPrice !== null && (
                        <div className="order-total">
                            <span>Загальна вартість</span>
                            <strong>{totalPrice} грн</strong>
                        </div>
                    )}

                    <button type="submit" className="btn btn-primary btn-block">
                        Підтвердити замовлення
                    </button>
                </form>
            </div>
        </div>
    )
}
