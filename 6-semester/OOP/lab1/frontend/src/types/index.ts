export type CarStatus   = 'AVAILABLE' | 'UNAVAILABLE'
export type OrderStatus = 'PENDING' | 'PAID' | 'ACTIVE' | 'RETURNED' | 'DAMAGED' | 'AWAITING_PAYMENT' | 'CLOSED' | 'REJECTED'

export interface Car {
    id: number
    brand: string
    model: string
    year: number
    pricePerDay: number
    status: CarStatus
    imageUrl?: string
}

export interface Order {
    id: number
    carId: number
    carBrand: string
    carModel: string
    clientName: string
    passportData: string
    startDate: string
    endDate: string
    totalPrice: number
    status: OrderStatus
    rejectionReason?: string
    repairInvoice?: RepairInvoice
    createdAt: string
}

export interface RepairInvoice {
    id: number
    damageDescription: string
    repairCost: number
    paid: boolean
}