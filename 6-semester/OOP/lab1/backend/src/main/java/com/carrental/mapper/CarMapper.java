package com.carrental.mapper;

import com.carrental.dto.CarDto;
import com.carrental.model.Car;
import org.mapstruct.Mapper;
import org.mapstruct.factory.Mappers;


@Mapper
public interface CarMapper {

    CarMapper INSTANCE = Mappers.getMapper(CarMapper.class);

    CarDto toDto(Car car);
    Car toModel(CarDto dto);
}