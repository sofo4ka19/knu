package com.carrental.mapper;

import com.carrental.dto.OrderResponseDto;
import com.carrental.model.Order;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper
public interface OrderMapper {

    OrderMapper INSTANCE = Mappers.getMapper(OrderMapper.class);

    @Mapping(source = "car.id",    target = "carId")
    @Mapping(source = "car.brand", target = "carBrand")
    @Mapping(source = "car.model", target = "carModel")
    @Mapping(source = "user.fullName", target = "clientName")
    OrderResponseDto toDto(Order order);
}