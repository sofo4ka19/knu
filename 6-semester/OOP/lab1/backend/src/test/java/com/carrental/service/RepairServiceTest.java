package com.carrental.service;

import com.carrental.dao.CarDao;
import com.carrental.dao.OrderDao;
import com.carrental.dao.RepairInvoiceDao;
import com.carrental.dto.RepairInvoiceDto;
import com.carrental.model.*;
import com.carrental.model.Order;
import com.carrental.model.enums.CarStatus;
import com.carrental.model.enums.OrderStatus;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RepairServiceTest {

    @Mock private RepairInvoiceDao repairDao;
    @Mock private OrderDao orderDao;
    @Mock private CarDao carDao;

    @InjectMocks
    private RepairService repairService;

    private Order returnedOrder;
    private RepairInvoiceDto invoiceDto;

    @BeforeEach
    void setUp() {
        Car car = Car.builder()
                .id(1L)
                .status(CarStatus.AVAILABLE)
                .build();

        returnedOrder = Order.builder()
                .id(10L)
                .car(car)
                .status(OrderStatus.RETURNED)
                .build();

        invoiceDto = new RepairInvoiceDto();
        invoiceDto.setDamageDescription("Подряпина на дверях");
        invoiceDto.setRepairCost(new BigDecimal("3000"));
    }

    @Test
    @DisplayName("Успішно створює рахунок для поверненого замовлення")
    void createInvoice_shouldSucceed_forReturnedOrder() {
        when(orderDao.findById(10L)).thenReturn(Optional.of(returnedOrder));
        when(repairDao.save(any())).thenAnswer(inv -> {
            RepairInvoice invoice = inv.getArgument(0);
            invoice.setId(1L);
            return invoice;
        });

        RepairInvoice result = repairService.createInvoice(10L, invoiceDto);

        assertEquals("Подряпина на дверях", result.getDamageDescription());
        assertEquals(new BigDecimal("3000"), result.getRepairCost());

        verify(carDao).updateStatus(1L, CarStatus.UNAVAILABLE);
        verify(orderDao).updateStatus(10L, OrderStatus.DAMAGED, null);
    }

    @Test
    @DisplayName("Не можна додати рахунок до активного замовлення")
    void createInvoice_shouldThrow_forActiveOrder() {
        returnedOrder.setStatus(OrderStatus.ACTIVE); // не RETURNED
        when(orderDao.findById(10L)).thenReturn(Optional.of(returnedOrder));

        assertThrows(IllegalStateException.class,
                () -> repairService.createInvoice(10L, invoiceDto));

        verify(repairDao, never()).save(any());
    }

    @Test
    @DisplayName("Кидає виняток якщо замовлення не існує")
    void createInvoice_shouldThrow_whenOrderNotFound() {
        when(orderDao.findById(99L)).thenReturn(Optional.empty());

        assertThrows(IllegalArgumentException.class,
                () -> repairService.createInvoice(99L, invoiceDto));
    }
}