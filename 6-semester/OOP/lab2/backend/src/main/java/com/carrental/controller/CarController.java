package com.carrental.controller;

import com.carrental.dto.CarDto;
import com.carrental.mapper.CarMapper;
import com.carrental.service.CarService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cars")
@RequiredArgsConstructor
public class CarController {

    private final CarService carService;
    private final CarMapper carMapper;

    @GetMapping
    public List<CarDto> getAll() {
        return carService.getAllCars().stream()
                .map(carMapper::toDto)
                .toList();
    }

    @GetMapping("/{id}")
    public CarDto getById(@PathVariable Long id) {
        return carMapper.toDto(carService.getCarById(id));
    }
}
