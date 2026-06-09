import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { createAuthApi } from '../api/apiClient'
import type { Order } from '../types'

const STATUS_LABELS: Record<string, string> = {
    PENDING:          '⏳ Очікує оплати',
    PAID:             '💳 Оплачено',
    ACTIVE:           '🚗 Активне',
    RETURNED:         '✅ Повернуто',
    DAMAGED:          '🔧 Пошкоджено',
    AWAITING_PAYMENT: '💰 Очікує оплати ремонту',
    CLOSED:           '✅ Завершено',
    REJECTED:         '❌ Відхилено',
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

    const handlePayRepair = async (orderId: number) => {
        await api.post(`/orders/${orderId}/pay-repair`)
        setOrders(prev => prev.map(o =>
            o.id === orderId && o.repairInvoice
                ? {...o, repairInvoice: {...o.repairInvoice, paid: true}}
                : o
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
                            <p>Вартість ремонту: <strong>{order.repairInvoice.repairCost} грн</strong></p>
                            {order.repairInvoice.paid
                                ? <p>✅ Ремонт оплачено</p>
                                : <button onClick={() => handlePayRepair(order.id)}>Оплатити ремонт</button>
                            }
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