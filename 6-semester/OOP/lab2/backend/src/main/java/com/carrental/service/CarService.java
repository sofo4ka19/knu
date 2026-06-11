package com.carrental.service;

import com.carrental.model.Car;
import com.carrental.model.enums.CarStatus;
import com.carrental.repository.CarRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class CarService {

    private final CarRepository carRepository;

    public List<Car> getAvailableCars() {
        return carRepository.findByStatusOrderByBrand(CarStatus.AVAILABLE);
    }

    public Car getCarById(Long id) {
        return carRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Car not found: " + id));
    }

    public List<Car> getAllCars() {
        return carRepository.findAllByOrderByBrandAscModelAsc();
    }
}
