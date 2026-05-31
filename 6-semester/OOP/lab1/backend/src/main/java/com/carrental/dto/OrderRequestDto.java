package com.carrental.dto;

import lombok.Data;
import java.time.LocalDate;

@Data
public class OrderRequestDto {
    private Long carId;
    private String passportData;
    private LocalDate startDate;
    private LocalDate endDate;
}