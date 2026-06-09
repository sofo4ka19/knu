package com.carrental.dto;

import lombok.Data;
import java.math.BigDecimal;

@Data
public class RepairInvoiceDto {
    private Long id;
    private String damageDescription;
    private BigDecimal repairCost;
    private boolean paid;
}