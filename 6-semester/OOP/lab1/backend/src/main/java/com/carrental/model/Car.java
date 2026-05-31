package com.carrental.model;

import com.carrental.model.enums.CarStatus;
import lombok.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Car {

    private Long id;
    private String brand;
    private String model;
    private Integer year;
    private String plateNumber;
    private BigDecimal pricePerDay;

    @Builder.Default
    private CarStatus status = CarStatus.AVAILABLE;

    private String imageUrl;
    private LocalDateTime createdAt;
}