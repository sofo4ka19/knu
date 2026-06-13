package com.carrental.service;

import com.carrental.dto.OrderRequestDto;
import com.carrental.model.Car;
import com.carrental.model.Order;
import com.carrental.model.User;
import com.carrental.model.enums.CarStatus;
import com.carrental.model.enums.OrderStatus;
import com.carrental.repository.CarRepository;
import com.carrental.repository.OrderRepository;
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

    @Mock private OrderRepository orderRepository;
    @Mock private CarRepository carRepository;

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
        dto.setEndDate(LocalDate.of(2024, 6, 6)); // 6 днів

        when(carRepository.findById(1L)).thenReturn(Optional.of(availableCar));
        when(orderRepository.hasConflict(anyLong(), any(LocalDate.class), any(LocalDate.class)))
                .thenReturn(false);
        when(orderRepository.save(any())).thenAnswer(inv -> {
            Order o = inv.getArgument(0);
            o.setId(99L);
            return o;
        });

        Order result = orderService.createOrder(dto, testUser);

        assertEquals(new BigDecimal("6000"), result.getTotalPrice()); // 1000 × 6
        assertEquals(OrderStatus.PENDING, result.getStatus());
    }

    @Test
    @DisplayName("Виняток якщо авто недоступне")
    void createOrder_shouldThrowWhenCarNotAvailable() {
        availableCar.setStatus(CarStatus.UNAVAILABLE);
        when(carRepository.findById(1L)).thenReturn(Optional.of(availableCar));

        OrderRequestDto dto = new OrderRequestDto();
        dto.setCarId(1L);
        dto.setPassportData("АА123456");
        dto.setStartDate(LocalDate.now());
        dto.setEndDate(LocalDate.now().plusDays(3));

        assertThrows(IllegalStateException.class,
                () -> orderService.createOrder(dto, testUser));
        verify(orderRepository, never()).save(any());
    }

    @Test
    @DisplayName("Виняток якщо кінцева дата раніше початкової")
    void createOrder_shouldThrowWhenEndDateBeforeStart() {
        when(carRepository.findById(1L)).thenReturn(Optional.of(availableCar));

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
        when(orderRepository.findById(1L)).thenReturn(Optional.of(paidOrder));

        assertThrows(IllegalStateException.class,
                () -> orderService.payOrder(1L, testUser.getId()));
    }

    @Test
    @DisplayName("Інший користувач не може оплатити чуже замовлення")
    void payOrder_shouldThrowForWrongUser() {
        Order order = Order.builder()
                .id(1L).user(testUser).status(OrderStatus.PENDING).build();
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

        assertThrows(SecurityException.class,
                () -> orderService.payOrder(1L, 999L));
    }
}
