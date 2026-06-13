import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { createAuthApi } from '../api/apiClient'
import type { Order } from '../types'

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

export default function MyOrdersPage() {
    const [orders, setOrders] = useState<Order[]>([])
    const [loading, setLoading] = useState(true)
    const { getAccessTokenSilently } = useAuth0()
    const api = createAuthApi(() => getAccessTokenSilently())

    useEffect(() => {
        api.get<Order[]>('/orders/my')
            .then(res => setOrders(res.data))
            .finally(() => setLoading(false))
    }, [])

    const handlePay = async (orderId: number) => {
        await api.post(`/orders/${orderId}/pay`)
        setOrders(prev => prev.map(o =>
            o.id === orderId ? { ...o, status: 'PAID' } : o
        ))
    }

    const handlePayRepair = async (orderId: number) => {
        await api.post(`/orders/${orderId}/pay-repair`)
        setOrders(prev => prev.map(o => {
            if (o.id !== orderId || !o.repairInvoice) return o
            const newStatus = o.status === 'AWAITING_PAYMENT' ? 'CLOSED' : o.status
            return { ...o, status: newStatus, repairInvoice: { ...o.repairInvoice, paid: true } }
        }))
    }

    if (loading) return <div className="loading">Завантаження замовлень...</div>

    return (
        <div>
            <h1>Мої замовлення</h1>
            {orders.length === 0 ? (
                <div className="empty-state">
                    <div className="empty-state-icon">📋</div>
                    <p>У вас поки немає замовлень</p>
                </div>
            ) : (
                <div className="orders-list">
                    {orders.map(order => (
                        <div key={order.id} className="order-card">
                            <div className="order-card-header">
                                <div className="order-card-title">{order.carBrand} {order.carModel}</div>
                                <span className={`badge badge-${order.status}`}>
                                    {STATUS_LABELS[order.status] ?? order.status}
                                </span>
                            </div>

                            <div className="order-card-dates">
                                📅 {order.startDate} — {order.endDate}
                            </div>
                            <div className="order-card-price">{order.totalPrice} грн</div>

                            {order.status === 'REJECTED' && order.rejectionReason && (
                                <div className="rejection">Причина відхилення: {order.rejectionReason}</div>
                            )}

                            {order.repairInvoice && (
                                <div className="repair-invoice">
                                    <span className="repair-invoice-label">🔧 Пошкодження</span>
                                    <span>{order.repairInvoice.damageDescription}</span>
                                    <span>Вартість ремонту: <strong>{order.repairInvoice.repairCost} грн</strong></span>
                                    {order.repairInvoice.paid
                                        ? <span className="repair-invoice-paid">✓ Ремонт оплачено</span>
                                        : (
                                            <div className="order-card-actions">
                                                <button className="btn btn-warning btn-sm"
                                                        onClick={() => handlePayRepair(order.id)}>
                                                    Оплатити ремонт
                                                </button>
                                            </div>
                                        )
                                    }
                                </div>
                            )}

                            {order.status === 'PENDING' && (
                                <div className="order-card-actions">
                                    <button className="btn btn-primary btn-sm"
                                            onClick={() => handlePay(order.id)}>
                                        Оплатити
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
