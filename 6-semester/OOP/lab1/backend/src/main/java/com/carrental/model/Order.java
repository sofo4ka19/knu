package com.carrental.model;

import com.carrental.model.enums.OrderStatus;
import lombok.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Order {

    private Long id;
    private Car car;
    private User user;
    private String passportData;
    private LocalDate startDate;
    private LocalDate endDate;
    private BigDecimal totalPrice;

    @Builder.Default
    private OrderStatus status = OrderStatus.PENDING;

    private String rejectionReason;
    private LocalDateTime createdAt;
    private RepairInvoice repairInvoice; // null if there is no damage
}