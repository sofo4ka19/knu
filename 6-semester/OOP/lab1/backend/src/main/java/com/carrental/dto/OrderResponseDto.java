package com.carrental.dto;

import com.carrental.model.enums.OrderStatus;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
public class OrderResponseDto {
    private Long id;
    private Long carId;
    private String carBrand;
    private String carModel;
    private String clientName;
    private String passportData;
    private LocalDate startDate;
    private LocalDate endDate;
    private BigDecimal totalPrice;
    private OrderStatus status;
    private String rejectionReason;
    private RepairInvoiceDto repairInvoice;
    private LocalDateTime createdAt;
}