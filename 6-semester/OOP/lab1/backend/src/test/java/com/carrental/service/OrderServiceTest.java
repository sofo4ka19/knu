package com.carrental.service;

import com.carrental.dao.CarDao;
import com.carrental.dao.OrderDao;
import com.carrental.dto.OrderRequestDto;
import com.carrental.model.*;
import com.carrental.model.Order;
import com.carrental.model.enums.*;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock private OrderDao orderDao;
    @Mock private CarDao   carDao;

    @InjectMocks private OrderService orderService;

    private Car availableCar;
    private User testUser;

    @BeforeEach
    void setUp() {
        availableCar = Car.builder()
                .id(1L).brand("Toyota").model("Camry")
                .pricePerDay(new BigDecimal("1000"))
                .status(CarStatus.AVAILABLE)
                .build();

        testUser = User.builder()
                .id(10L).email("test@test.com").auth0Id("auth0|abc")
                .build();
    }

    @Test
    @DisplayName("Ціна замовлення = кількість днів × ціна за день")
    void createOrder_shouldCalculateTotalPrice() {
        OrderRequestDto dto = new OrderRequestDto();
        dto.setCarId(1L);
        dto.setPassportData("АА123456");
        dto.setStartDate(LocalDate.of(2024, 6, 1));
        dto.setEndDate(LocalDate.of(2024, 6, 6)); // 5 днів

        when(carDao.findById(1L)).thenReturn(Optional.of(availableCar));
        when(orderDao.save(any())).thenAnswer(inv -> {
            Order o = inv.getArgument(0);
            o.setId(99L);
            return o;
        });

        Order result = orderService.createOrder(dto, testUser);

        assertEquals(new BigDecimal("5000"), result.getTotalPrice()); // 1000 × 5
        assertEquals(OrderStatus.PENDING, result.getStatus());
        verify(carDao).updateStatus(1L, CarStatus.RENTED);
    }

    @Test
    @DisplayName("Виняток якщо авто вже зайняте")
    void createOrder_shouldThrowWhenCarNotAvailable() {
        availableCar.setStatus(CarStatus.RENTED);
        when(carDao.findById(1L)).thenReturn(Optional.of(availableCar));

        OrderRequestDto dto = new OrderRequestDto();
        dto.setCarId(1L);
        dto.setStartDate(LocalDate.now());
        dto.setEndDate(LocalDate.now().plusDays(3));

        assertThrows(IllegalStateException.class,
                () -> orderService.createOrder(dto, testUser));
        verify(orderDao, never()).save(any());
    }

    @Test
    @DisplayName("Виняток якщо кінцева дата раніше початкової")
    void createOrder_shouldThrowWhenEndDateBeforeStart() {
        when(carDao.findById(1L)).thenReturn(Optional.of(availableCar));

        OrderRequestDto dto = new OrderRequestDto();
        dto.setCarId(1L);
        dto.setPassportData("АА123456");
        dto.setStartDate(LocalDate.of(2024, 6, 10));
        dto.setEndDate(LocalDate.of(2024, 6, 5)); // кінець раніше початку

        assertThrows(IllegalArgumentException.class,
                () -> orderService.createOrder(dto, testUser));
    }

    @Test
    @DisplayName("Оплатити можна тільки PENDING замовлення")
    void payOrder_shouldThrowIfNotPending() {
        Order paidOrder = Order.builder()
                .id(1L).user(testUser).status(OrderStatus.PAID).build();
        when(orderDao.findById(1L)).thenReturn(Optional.of(paidOrder));

        assertThrows(IllegalStateException.class,
                () -> orderService.payOrder(1L, testUser.getId()));
    }

    @Test
    @DisplayName("Інший користувач не може оплатити чуже замовлення")
    void payOrder_shouldThrowForWrongUser() {
        Order order = Order.builder()
                .id(1L).user(testUser).status(OrderStatus.PENDING).build();
        when(orderDao.findById(1L)).thenReturn(Optional.of(order));

        assertThrows(SecurityException.class,
                () -> orderService.payOrder(1L, 999L));
    }
}