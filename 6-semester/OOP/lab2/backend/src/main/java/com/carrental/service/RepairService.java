package com.carrental.service;

import com.carrental.dto.RepairInvoiceDto;
import com.carrental.model.Order;
import com.carrental.model.RepairInvoice;
import com.carrental.model.enums.CarStatus;
import com.carrental.model.enums.OrderStatus;
import com.carrental.repository.CarRepository;
import com.carrental.repository.OrderRepository;
import com.carrental.repository.RepairInvoiceRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Slf4j
@Service
@RequiredArgsConstructor
public class RepairService {

    private final RepairInvoiceRepository repairInvoiceRepository;
    private final OrderRepository orderRepository;
    private final CarRepository carRepository;

    @Transactional
    public RepairInvoice createInvoice(Long orderId, RepairInvoiceDto dto) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

        if (order.getStatus() != OrderStatus.RETURNED) {
            throw new IllegalStateException("Can only create repair invoice for RETURNED orders");
        }

        RepairInvoice invoice = RepairInvoice.builder()
                .order(order)
                .damageDescription(dto.getDamageDescription())
                .repairCost(dto.getRepairCost())
                .build();

        RepairInvoice saved = repairInvoiceRepository.save(invoice);

        order.setStatus(OrderStatus.DAMAGED);
        orderRepository.save(order);

        order.getCar().setStatus(CarStatus.UNAVAILABLE);
        carRepository.save(order.getCar());

        log.info("Repair invoice created for order {}, cost: {}", orderId, dto.getRepairCost());
        return saved;
    }

    @Transactional
    public void payRepair(Long orderId) {
        RepairInvoice invoice = repairInvoiceRepository.findByOrderId(orderId)
                .orElseThrow(() -> new IllegalArgumentException(
                        "No repair invoice for order: " + orderId));

        if (invoice.isPaid()) {
            throw new IllegalStateException("Repair invoice already paid");
        }

        invoice.setPaid(true);
        repairInvoiceRepository.save(invoice);

        Order order = invoice.getOrder();
        order.setStatus(OrderStatus.CLOSED);
        orderRepository.save(order);

        log.info("Repair invoice paid for order {}, order closed", orderId);
    }
}
