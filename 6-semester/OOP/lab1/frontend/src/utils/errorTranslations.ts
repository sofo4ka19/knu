const TRANSLATIONS: [string, string][] = [
    // OrderService
    ['Car not found',                                           'Автомобіль не знайдено'],
    ['Invalid passport format',                                 'Невірний формат паспорта. Очікується: АБ123456, FF123456 або 123456789'],
    ['Car is not available for rent',                           'Автомобіль недоступний для оренди'],
    ['End date must be on or after start date',                 'Дата закінчення не може бути раніше дати початку'],
    ['Car is already booked for the selected dates',            'Автомобіль вже заброньований на вибрані дати'],
    ['Only PENDING orders can be paid',                        'Оплатити можна лише замовлення зі статусом «Очікує оплати»'],
    ['Only PAID orders can be activated',                       'Видати можна лише оплачене замовлення'],
    ['Only ACTIVE orders can be returned',                      'Повернення можливе лише для активного замовлення'],
    ['Rejection reason is required',                            'Необхідно вказати причину відхилення'],
    ['Only PENDING or PAID orders can be rejected',            'Відхилити можна лише замовлення зі статусом «Очікує оплати» або «Оплачено»'],
    ['Only RETURNED orders can be completed',                   'Завершити можна лише повернуте замовлення'],
    ['Only DAMAGED orders can be restored',                     'Відновити можна лише пошкоджене замовлення'],
    ['Order not found',                                         'Замовлення не знайдено'],
    ['Access denied to order',                                  'Немає доступу до замовлення'],
    // RepairService
    ['Can only create repair invoice for RETURNED orders',      'Акт про пошкодження можна створити лише для поверненого замовлення'],
    ['No repair invoice for order',                             'Рахунок на ремонт не знайдено'],
    ['Repair invoice already paid',                             'Рахунок на ремонт вже оплачено'],
    // Filters
    ['Authorization header missing',                            'Відсутній заголовок авторизації'],
    ['Invalid token',                                           'Недійсний токен авторизації'],
    ['Admin access required',                                   'Доступ лише для адміністраторів'],
    // Servlets
    ['Invalid car id',                                          'Невірний ідентифікатор автомобіля'],
    ['Not found',                                               'Сторінку не знайдено'],
    ['Admin endpoint not found',                                'Сторінку не знайдено'],
]

export function translateError(msg: string): string {
    for (const [key, ua] of TRANSLATIONS) {
        if (msg.startsWith(key)) return ua
    }
    return msg
}
