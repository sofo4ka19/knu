package com.carrental.service;

import com.carrental.dto.OrderRequestDto;
import com.carrental.model.Car;
import com.carrental.model.Order;
import com.carrental.model.User;
import com.carrental.model.enums.CarStatus;
import com.carrental.model.enums.OrderStatus;
import com.carrental.repository.CarRepository;
import com.carrental.repository.OrderRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.regex.Pattern;

@Slf4j
@Service
@RequiredArgsConstructor
public class OrderService {

    private static final Pattern PASSPORT_RE =
            Pattern.compile("^([А-ЯІЇЄ]{2}\\d{6}|[A-Z]{2}\\d{6}|\\d{9})$");

    private final OrderRepository orderRepository;
    private final CarRepository carRepository;

    @Transactional
    public Order createOrder(OrderRequestDto dto, User currentUser) {
        Car car = carRepository.findById(dto.getCarId())
                .orElseThrow(() -> new IllegalArgumentException("Car not found: " + dto.getCarId()));

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

        if (orderRepository.hasConflict(car.getId(), dto.getStartDate(), dto.getEndDate())) {
            throw new IllegalStateException("Car is already booked for the selected dates");
        }

        long days = ChronoUnit.DAYS.between(dto.getStartDate(), dto.getEndDate()) + 1;
        BigDecimal totalPrice = car.getPricePerDay().multiply(BigDecimal.valueOf(days));

        Order order = Order.builder()
                .car(car)
                .user(currentUser)
                .passportData(dto.getPassportData())
                .startDate(dto.getStartDate())
                .endDate(dto.getEndDate())
                .totalPrice(totalPrice)
                .status(OrderStatus.PENDING)
                .build();

        Order saved = orderRepository.save(order);
        log.info("Order {} created by user {}", saved.getId(), currentUser.getId());
        return saved;
    }

    @Transactional
    public Order payOrder(Long orderId, Long currentUserId) {
        Order order = getOrderOrThrow(orderId);
        verifyOwner(order, currentUserId);

        if (order.getStatus() != OrderStatus.PENDING) {
            throw new IllegalStateException(
                    "Only PENDING orders can be paid. Current: " + order.getStatus());
        }

        order.setStatus(OrderStatus.PAID);
        log.info("Order {} paid by user {}", orderId, currentUserId);
        return orderRepository.save(order);
    }

    @Transactional
    public Order activateOrder(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.PAID) {
            throw new IllegalStateException("Only PAID orders can be activated");
        }
        order.setStatus(OrderStatus.ACTIVE);
        return orderRepository.save(order);
    }

    @Transactional
    public Order returnCar(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.ACTIVE) {
            throw new IllegalStateException("Only ACTIVE orders can be returned");
        }
        order.setStatus(OrderStatus.RETURNED);
        log.info("Car {} returned from order {}", order.getCar().getId(), orderId);
        return orderRepository.save(order);
    }

    @Transactional
    public Order rejectOrder(Long orderId, String reason) {
        if (reason == null || reason.isBlank()) {
            throw new IllegalArgumentException("Rejection reason is required");
        }
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.PENDING && order.getStatus() != OrderStatus.PAID) {
            throw new IllegalStateException(
                    "Only PENDING or PAID orders can be rejected. Current: " + order.getStatus());
        }
        order.setStatus(OrderStatus.REJECTED);
        order.setRejectionReason(reason);
        return orderRepository.save(order);
    }

    @Transactional
    public Order completeOrder(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.RETURNED) {
            throw new IllegalStateException("Only RETURNED orders can be completed");
        }
        order.setStatus(OrderStatus.CLOSED);
        log.info("Order {} completed without damage", orderId);
        return orderRepository.save(order);
    }

    @Transactional
    public Order restoreCarAfterRepair(Long orderId) {
        Order order = getOrderOrThrow(orderId);
        if (order.getStatus() != OrderStatus.DAMAGED) {
            throw new IllegalStateException("Only DAMAGED orders can be restored");
        }
        Car car = order.getCar();
        car.setStatus(CarStatus.AVAILABLE);
        carRepository.save(car);

        // Flow 1: user already paid → close immediately
        // Flow 2: user hasn't paid yet → wait for payment
        boolean invoicePaid = order.getRepairInvoice() != null && order.getRepairInvoice().isPaid();
        order.setStatus(invoicePaid ? OrderStatus.CLOSED : OrderStatus.AWAITING_PAYMENT);
        log.info("Car {} restored for order {}, invoice paid: {}", car.getId(), orderId, invoicePaid);
        return orderRepository.save(order);
    }

    public List<Order> getMyOrders(Long userId) {
        log.info("Getting orders for user {}", userId);
        return orderRepository.findByUserIdWithDetails(userId);
    }

    public List<Order> getAllOrders() {
        return orderRepository.findAllWithDetails();
    }

    public void verifyOwnerPublic(Long orderId, Long userId) {
        verifyOwner(getOrderOrThrow(orderId), userId);
    }

    private Order getOrderOrThrow(Long orderId) {
        return orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
    }

    private void verifyOwner(Order order, Long userId) {
        if (!order.getUser().getId().equals(userId)) {
            throw new SecurityException("Access denied to order " + order.getId());
        }
    }
}
