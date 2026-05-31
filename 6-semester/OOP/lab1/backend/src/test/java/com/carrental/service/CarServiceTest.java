package com.carrental.service;

import com.carrental.dao.CarDao;
import com.carrental.model.Car;
import com.carrental.model.enums.CarStatus;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.*;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CarServiceTest {

    @Mock
    private CarDao carDao;

    @InjectMocks
    private CarService carService;

    private Car availableCar;
    private Car rentedCar;

    @BeforeEach
    void setUp() {
        availableCar = Car.builder()
                .id(1L).brand("Toyota").model("Camry")
                .pricePerDay(new BigDecimal("1000"))
                .status(CarStatus.AVAILABLE)
                .build();

        rentedCar = Car.builder()
                .id(2L).brand("BMW").model("X5")
                .pricePerDay(new BigDecimal("2000"))
                .status(CarStatus.RENTED)
                .build();
    }

    @Test
    @DisplayName("Повертає тільки доступні авто")
    void getAvailableCars_shouldReturnOnlyAvailable() {
        when(carDao.findByStatus(CarStatus.AVAILABLE))
                .thenReturn(List.of(availableCar));

        List<Car> result = carService.getAvailableCars();

        assertEquals(1, result.size());
        assertEquals(CarStatus.AVAILABLE, result.get(0).getStatus());
        // перевіряємо що викликали саме з AVAILABLE, не з RENTED
        verify(carDao).findByStatus(CarStatus.AVAILABLE);
    }

    @Test
    @DisplayName("Повертає авто якщо існує")
    void getCarById_shouldReturnCar_whenExists() {
        when(carDao.findById(1L)).thenReturn(Optional.of(availableCar));

        Car result = carService.getCarById(1L);

        assertEquals("Toyota", result.getBrand());
        assertEquals("Camry", result.getModel());
    }

    @Test
    @DisplayName("Кидає виняток якщо авто не знайдено")
    void getCarById_shouldThrow_whenNotFound() {
        when(carDao.findById(99L)).thenReturn(Optional.empty());

        IllegalArgumentException ex = assertThrows(
                IllegalArgumentException.class,
                () -> carService.getCarById(99L)
        );

        assertTrue(ex.getMessage().contains("99"));
    }
}