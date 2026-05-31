import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { createAuthApi } from '../api/apiClient'
import type { Order } from '../types'

const STATUS_LABELS: Record<string, string> = {
    PENDING:  '⏳ Очікує оплати',
    PAID:     '💳 Оплачено',
    ACTIVE:   '🚗 Активне',
    RETURNED: '✅ Повернуто',
    DAMAGED:  '🔧 Пошкоджено',
    REJECTED: '❌ Відхилено',
}

export default function MyOrdersPage() {
    const [orders, setOrders] = useState<Order[]>([])
    const { getAccessTokenSilently } = useAuth0()

    const api = createAuthApi(() => getAccessTokenSilently())

    useEffect(() => {
        api.get<Order[]>('/orders/my').then(res => setOrders(res.data))
    }, [])

    const handlePay = async (orderId: number) => {
        await api.post(`/orders/${orderId}/pay`)
        setOrders(prev => prev.map(o =>
            o.id === orderId ? {...o, status: 'PAID'} : o
        ))
    }

    return (
        <div>
            <h1>Мої замовлення</h1>
            {orders.length === 0 && <p>У вас поки немає замовлень</p>}
            {orders.map(order => (
                <div key={order.id} className="order-card">
                    <h3>{order.carBrand} {order.carModel}</h3>
                    <p>{order.startDate} — {order.endDate}</p>
                    <p>Вартість: <strong>{order.totalPrice} грн</strong></p>
                    <p>Статус: {STATUS_LABELS[order.status] ?? order.status}</p>

                    {order.status === 'REJECTED' && order.rejectionReason && (
                        <p className="rejection">Причина: {order.rejectionReason}</p>
                    )}

                    {order.repairInvoice && (
                        <div className="repair-invoice">
                            <p>🔧 Пошкодження: {order.repairInvoice.damageDescription}</p>
                            <p>Вартість ремонту: {order.repairInvoice.repairCost} грн</p>
                        </div>
                    )}

                    {order.status === 'PENDING' && (
                        <button onClick={() => handlePay(order.id)}>Оплатити</button>
                    )}
                </div>
            ))}
        </div>
    )
}