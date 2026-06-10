import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { createAuthApi } from '../../api/apiClient'
import type { Order } from '../../types'

const STATUS_LABELS: Record<string, string> = {
    PENDING:          'Очікує оплати',
    PAID:             'Оплачено',
    ACTIVE:           'Активне',
    RETURNED:         'Повернуто',
    DAMAGED:          'Пошкоджено',
    AWAITING_PAYMENT: 'Очікує оплати ремонту',
    CLOSED:           'Завершено',
    REJECTED:         'Відхилено',
}

export default function AdminDashboard() {
    const [orders, setOrders] = useState<Order[]>([])
    const [loading, setLoading] = useState(true)
    const { getAccessTokenSilently } = useAuth0()
    const api = createAuthApi(() => getAccessTokenSilently())

    const refresh = () =>
        api.get<Order[]>('/admin/orders')
            .then(res => setOrders(res.data))
            .finally(() => setLoading(false))

    useEffect(() => { refresh() }, [])

    const activate  = (id: number) => api.post(`/admin/orders/${id}/activate`).then(refresh)
    const returnCar = (id: number) => api.post(`/admin/orders/${id}/return`).then(refresh)
    const complete  = (id: number) => api.post(`/admin/orders/${id}/complete`).then(refresh)
    const restoreCar = (id: number) => api.post(`/admin/orders/${id}/restore`).then(refresh)

    const reject = async (id: number) => {
        const reason = prompt('Причина відхилення:')
        if (reason) api.post(`/admin/orders/${id}/reject`, { reason }).then(refresh)
    }

    const addDamage = async (id: number) => {
        const desc = prompt('Опис пошкоджень:')
        const cost = prompt('Вартість ремонту (грн):')
        if (desc && cost) {
            api.post(`/admin/orders/${id}/damage`, {
                damageDescription: desc,
                repairCost: Number(cost),
            }).then(refresh)
        }
    }

    if (loading) return <div className="loading">Завантаження замовлень...</div>

    return (
        <div>
            <h1>Панель адміністратора</h1>
            {orders.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">📋</div>
                    <p>Замовлень поки немає</p>
                </div>
            ) : (
                <div className="admin-table-wrap">
                    <table className="admin-table">
                        <thead>
                        <tr>
                            <th>Клієнт</th>
                            <th>Автомобіль</th>
                            <th>Період</th>
                            <th>Статус</th>
                            <th>Дії</th>
                        </tr>
                        </thead>
                        <tbody>
                        {orders.map(o => (
                            <tr key={o.id}>
                                <td>{o.passportData || '—'}</td>
                                <td>{o.carBrand} {o.carModel}</td>
                                <td style={{ whiteSpace: 'nowrap' }}>{o.startDate} — {o.endDate}</td>
                                <td>
                                    <span className={`badge badge-${o.status}`}>
                                        {STATUS_LABELS[o.status] ?? o.status}
                                    </span>
                                </td>
                                <td>
                                    <div className="actions">
                                        {o.status === 'PAID' && (
                                            <button className="btn btn-success btn-sm" onClick={() => activate(o.id)}>
                                                Видати
                                            </button>
                                        )}
                                        {o.status === 'ACTIVE' && (
                                            <button className="btn btn-ghost btn-sm" onClick={() => returnCar(o.id)}>
                                                Повернення
                                            </button>
                                        )}
                                        {o.status === 'RETURNED' && (
                                            <>
                                                <button className="btn btn-success btn-sm" onClick={() => complete(o.id)}>
                                                    Завершити
                                                </button>
                                                <button className="btn btn-ghost btn-sm" onClick={() => addDamage(o.id)}>
                                                    Пошкодження
                                                </button>
                                            </>
                                        )}
                                        {o.status === 'DAMAGED' && (
                                            <>
                                                <span className="actions-note">
                                                    {o.repairInvoice?.paid ? '✓ Оплачено' : '⏳ Не оплачено'}
                                                </span>
                                                <button className="btn btn-primary btn-sm" onClick={() => restoreCar(o.id)}>
                                                    Відновити авто
                                                </button>
                                            </>
                                        )}
                                        {o.status === 'AWAITING_PAYMENT' && (
                                            <span className="actions-note">
                                                {o.repairInvoice?.paid ? '✓ Оплачено клієнтом' : '⏳ Очікує оплати клієнтом'}
                                            </span>
                                        )}
                                        {(o.status === 'PENDING' || o.status === 'PAID') && (
                                            <button className="btn btn-danger btn-sm" onClick={() => reject(o.id)}>
                                                Відхилити
                                            </button>
                                        )}
                                    </div>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}
