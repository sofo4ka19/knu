package com.carrental.service;

import com.carrental.dao.CarDao;
import com.carrental.dao.OrderDao;
import com.carrental.dto.OrderRequestDto;
import com.carrental.model.Car;
import com.carrental.model.Order;
import com.carrental.model.User;
import com.carrental.model.enums.CarStatus;
import com.carrental.model.enums.OrderStatus;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.regex.Pattern;

public class OrderService {

    private static final Logger log = LogManager.getLogger(OrderService.class);
    private static final Pattern PASSPORT_RE =
            Pattern.compile("^([А-ЯІЇЄ]{2}\\d{6}|[A-Z]{2}\\d{6}|\\d{9})$");
    private final OrderDao orderDao;
    private final CarDao carDao;

    public OrderService() {
        this.orderDao = new OrderDao();
        this.carDao = new CarDao();
    }

    public OrderService(OrderDao orderDao, CarDao carDao) {
        this.orderDao = orderDao;
        this.carDao = carDao;
    }

    public Order createOrder(OrderRequestDto dto, User currentUser) {
        Car car = carDao.findById(dto.getCarId())
                .orElseThrow(() -> new IllegalArgumentException(
                        "Car not found: " + dto.getCarId()));

        if (dto.getPassportData() == null ||
                !PASSPORT_RE.matcher(dto.getPassportData().trim().toUpperCase()).matches()) {
            throw new IllegalArgumentException(
                    "Invalid passport format. Expected: АБ123456, FF123456, or 123456789");
        }

        if (car.getStatus() == CarStatus.UNAVAILABLE) {
            throw new IllegalStateException("Car is not available for rent");
        }

        if (dto.getEndDate().isBefore(dto.getStartDate())) {
            throw new IllegalArgumentException("End date must be on or after start date");
        }

        long days = ChronoUnit.DAYS.between(dto.getStartDate(), dto.getEndDate()) + 1;

        if (orderDao.hasConflict(car.getId(), dto.getStartDate(), dto.getEndDate())) {
            throw new IllegalStateException("Car is already booked for the selected dates");
        }

        BigDecimal totalPrice = car.getPricePerDay()
                .multiply(BigDecimal.valueOf(days));

        Order order = Order.builder()
                .car(car)
                .user(currentUser)
                .passportData(dto.getPassportData())
                .startDate(dto.getStartDate())
                .endDate(dto.getEndDate())
                .totalPrice(totalPrice)
                .status(OrderStatus.PENDING)
                .createdAt(LocalDateTime.now())
                .build();

        Order saved = orderDao.save(order);
        log.info("Order {} created by user {}", saved.getId(), currentUser.getId());
        return saved;
    }

    public Order payOrder(Long orderId, Long currentUserId) {
        Order order = getOrderOrThrow(orderId);
        verifyOwner(order, currentUserId);

        if (order.getStatus() != OrderStatus.PENDING) {
            throw new IllegalStateException(
                    "Only PENDING orders can be paid. Current: " + order.getStatus());
        }

        orderDao.updateStatus(orderId, OrderStatus.PAID, null);
        order.setStatus(OrderStatus.PAID);
        log.info("Order {} paid by user {}", orderId, currentUserId);
        return order;
    }

    // ADMIN: confirm reservation
    public Order activateOrder(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.PAID) {
            throw new IllegalStateException("Only PAID orders can be activated");
        }
        orderDao.updateStatus(orderId, OrderStatus.ACTIVE, null);
        order.setStatus(OrderStatus.ACTIVE);
        return order;
    }

    // ADMIN: register returning
    public Order returnCar(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.ACTIVE) {
            throw new IllegalStateException("Only ACTIVE orders can be returned");
        }
        orderDao.updateStatus(orderId, OrderStatus.RETURNED, null);
        order.setStatus(OrderStatus.RETURNED);
        log.info("Car {} returned from order {}", order.getCar().getId(), orderId);
        return order;
    }

    // ADMIN: deny the order
    public Order rejectOrder(Long orderId, String reason) {
        if (reason == null || reason.isBlank()) {
            throw new IllegalArgumentException("Rejection reason is required");
        }
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.PENDING && order.getStatus() != OrderStatus.PAID) {
            throw new IllegalStateException(
                    "Only PENDING or PAID orders can be rejected. Current: " + order.getStatus());
        }
        orderDao.updateStatus(orderId, OrderStatus.REJECTED, reason);
        order.setStatus(OrderStatus.REJECTED);
        order.setRejectionReason(reason);
        return order;
    }

    // ADMIN: complete order without damage
    public Order completeOrder(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.RETURNED) {
            throw new IllegalStateException("Only RETURNED orders can be completed");
        }
        orderDao.updateStatus(orderId, OrderStatus.CLOSED, null);
        order.setStatus(OrderStatus.CLOSED);
        log.info("Order {} completed without damage", orderId);
        return order;
    }

    // ADMIN: restore car to available after repair (regardless of invoice payment)
    public Order restoreCarAfterRepair(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.DAMAGED) {
            throw new IllegalStateException("Only DAMAGED orders can be restored");
        }
        carDao.updateStatus(order.getCar().getId(), CarStatus.AVAILABLE);
        orderDao.updateStatus(orderId, OrderStatus.AWAITING_PAYMENT, null);
        order.setStatus(OrderStatus.AWAITING_PAYMENT);
        log.info("Car {} restored to AVAILABLE after repair for order {}", order.getCar().getId(), orderId);
        return order;
    }

    public List<Order> getMyOrders(Long userId) {
        return orderDao.findByUserId(userId);
    }

    public List<Order> getAllOrders() {
        return orderDao.findAll();
    }

    private Order getOrderOrThrow(Long orderId) {
        return orderDao.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException(
                        "Order not found: " + orderId));
    }

    public void verifyOwnerPublic(Long orderId, Long userId) {
        verifyOwner(getOrderOrThrow(orderId), userId);
    }

    private void verifyOwner(Order order, Long userId) {
        if (!order.getUser().getId().equals(userId)) {
            throw new SecurityException("Access denied to order " + order.getId());
        }
    }
}