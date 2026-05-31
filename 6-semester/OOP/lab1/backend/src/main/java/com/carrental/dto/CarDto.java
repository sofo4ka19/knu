package com.carrental.dto;

import com.carrental.model.enums.CarStatus;
import lombok.Data;
import java.math.BigDecimal;

@Data
public class CarDto {
    private Long id;
    private String brand;
    private String model;
    private Integer year;
    private BigDecimal pricePerDay;
    private CarStatus status;
    private String imageUrl;
}