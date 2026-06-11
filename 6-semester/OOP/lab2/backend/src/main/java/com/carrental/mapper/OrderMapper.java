package com.carrental.mapper;

import com.carrental.dto.OrderResponseDto;
import com.carrental.dto.RepairInvoiceDto;
import com.carrental.model.Order;
import com.carrental.model.RepairInvoice;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface OrderMapper {

    @Mapping(source = "car.id", target = "carId")
    @Mapping(source = "car.brand", target = "carBrand")
    @Mapping(source = "car.model", target = "carModel")
    @Mapping(source = "user.fullName", target = "clientName")
    OrderResponseDto toDto(Order order);

    RepairInvoiceDto toDto(RepairInvoice repairInvoice);
}
