package com.carrental.mapper;

import com.carrental.dto.CarDto;
import com.carrental.model.Car;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring")
public interface CarMapper {
    CarDto toDto(Car car);
    Car toModel(CarDto dto);
}
