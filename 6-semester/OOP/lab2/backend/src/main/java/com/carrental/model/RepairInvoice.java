package com.carrental.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "repair_invoices")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RepairInvoice {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Lab1 stored a bare Long orderId. Here we use a real relationship:
    // repair_invoices.order_id is the FK column, and it's UNIQUE (one invoice per order).
    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false, unique = true)
    private Order order;

    @Column(name = "damage_description", nullable = false, columnDefinition = "TEXT")
    private String damageDescription;

    @Column(name = "repair_cost", nullable = false, precision = 10, scale = 2)
    private BigDecimal repairCost;

    @Column(nullable = false)
    private boolean paid;

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
}
