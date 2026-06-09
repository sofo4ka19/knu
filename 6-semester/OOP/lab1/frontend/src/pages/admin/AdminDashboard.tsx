import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { createAuthApi } from '../../api/apiClient'
import type { Order } from '../../types'

export default function AdminDashboard() {
    const [orders, setOrders] = useState<Order[]>([])
    const { getAccessTokenSilently } = useAuth0()
    const api = createAuthApi(() => getAccessTokenSilently())

    const refresh = () =>
        api.get<Order[]>('/admin/orders').then(res => setOrders(res.data))

    useEffect(() => { refresh() }, [])

    const activate = (id: number) =>
        api.post(`/admin/orders/${id}/activate`).then(refresh)

    const returnCar = (id: number) =>
        api.post(`/admin/orders/${id}/return`).then(refresh)

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

    return (
        <div>
            <h1>Панель адміністратора</h1>
            <table className="admin-table">
                <thead>
                <tr>
                    <th>Паспорт</th><th>Авто</th>
                    <th>Період</th><th>Статус</th><th>Дії</th>
                </tr>
                </thead>
                <tbody>
                {orders.map(o => (
                    <tr key={o.id}>
                        <td>{o.passportData}</td>
                        <td>{o.carBrand} {o.carModel}</td>
                        <td>{o.startDate} — {o.endDate}</td>
                        <td>{o.status}</td>
                        <td className="actions">
                            {o.status === 'PAID'     && <button onClick={() => activate(o.id)}>Видати</button>}
                            {o.status === 'ACTIVE'   && <button onClick={() => returnCar(o.id)}>Повернення</button>}
                            {o.status === 'RETURNED' && <button onClick={() => addDamage(o.id)}>Пошкодження</button>}
                            {(o.status === 'PENDING' || o.status === 'PAID') && <button onClick={() => reject(o.id)}>Відхилити</button>}
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    )
}