package com.carrental.service;

import com.carrental.dao.CarDao;
import com.carrental.dao.OrderDao;
import com.carrental.dao.RepairInvoiceDao;
import com.carrental.dto.RepairInvoiceDto;
import com.carrental.model.Order;
import com.carrental.model.RepairInvoice;
import com.carrental.model.enums.CarStatus;
import com.carrental.model.enums.OrderStatus;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.time.LocalDateTime;

public class RepairService {

    private static final Logger log = LogManager.getLogger(RepairService.class);
    private final RepairInvoiceDao repairDao = new RepairInvoiceDao();
    private final OrderDao         orderDao  = new OrderDao();
    private final CarDao           carDao    = new CarDao();

    public RepairInvoice createInvoice(Long orderId, RepairInvoiceDto dto) {
        Order order = orderDao.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException(
                        "Order not found: " + orderId));

        if (order.getStatus() != OrderStatus.RETURNED) {
            throw new IllegalStateException(
                    "Can only create repair invoice for RETURNED orders");
        }

        RepairInvoice invoice = RepairInvoice.builder()
                .orderId(orderId)
                .damageDescription(dto.getDamageDescription())
                .repairCost(dto.getRepairCost())
                .createdAt(LocalDateTime.now())
                .build();

        RepairInvoice saved = repairDao.save(invoice);
        // Change order and car status
        orderDao.updateStatus(orderId, OrderStatus.DAMAGED, null);
        carDao.updateStatus(order.getCar().getId(), CarStatus.UNAVAILABLE);
        log.info("Repair invoice created for order {}, cost: {}",
                orderId, dto.getRepairCost());
        return saved;
    }
}