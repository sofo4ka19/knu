package com.carrental.service;

import com.carrental.dto.RepairInvoiceDto;
import com.carrental.model.Car;
import com.carrental.model.Order;
import com.carrental.model.RepairInvoice;
import com.carrental.model.enums.CarStatus;
import com.carrental.model.enums.OrderStatus;
import com.carrental.repository.CarRepository;
import com.carrental.repository.OrderRepository;
import com.carrental.repository.RepairInvoiceRepository;
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

    @Mock private RepairInvoiceRepository repairInvoiceRepository;
    @Mock private OrderRepository orderRepository;
    @Mock private CarRepository carRepository;

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
        when(orderRepository.findById(10L)).thenReturn(Optional.of(returnedOrder));
        when(repairInvoiceRepository.save(any())).thenAnswer(inv -> {
            RepairInvoice invoice = inv.getArgument(0);
            invoice.setId(1L);
            return invoice;
        });
        when(orderRepository.save(any())).thenAnswer(inv -> inv.getArgument(0));
        when(carRepository.save(any())).thenAnswer(inv -> inv.getArgument(0));

        RepairInvoice result = repairService.createInvoice(10L, invoiceDto);

        assertEquals("Подряпина на дверях", result.getDamageDescription());
        assertEquals(new BigDecimal("3000"), result.getRepairCost());

        verify(orderRepository).save(argThat(o -> o.getStatus() == OrderStatus.DAMAGED));
        verify(carRepository).save(argThat(c -> c.getStatus() == CarStatus.UNAVAILABLE));
    }

    @Test
    @DisplayName("Не можна додати рахунок до активного замовлення")
    void createInvoice_shouldThrow_forActiveOrder() {
        returnedOrder.setStatus(OrderStatus.ACTIVE);
        when(orderRepository.findById(10L)).thenReturn(Optional.of(returnedOrder));

        assertThrows(IllegalStateException.class,
                () -> repairService.createInvoice(10L, invoiceDto));

        verify(repairInvoiceRepository, never()).save(any());
    }

    @Test
    @DisplayName("Кидає виняток якщо замовлення не існує")
    void createInvoice_shouldThrow_whenOrderNotFound() {
        when(orderRepository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(IllegalArgumentException.class,
                () -> repairService.createInvoice(99L, invoiceDto));
    }
}
