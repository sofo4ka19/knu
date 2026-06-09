package com.carrental.model;

import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RepairInvoice {

    private Long id;
    private Long orderId;
    private String damageDescription;
    private BigDecimal repairCost;
    private boolean paid;
    private LocalDateTime createdAt;
}