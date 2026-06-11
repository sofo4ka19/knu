package com.carrental.repository;

import com.carrental.model.Order;
import com.carrental.model.enums.OrderStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.time.LocalDate;
import java.util.List;

public interface OrderRepository extends JpaRepository<Order, Long> {

    // JOIN FETCH loads car, user, and repairInvoice in one SQL query.
    // Without this, Hibernate would fire a separate SELECT for each
    // lazy association on every row — the N+1 problem lab1's DAO had.
    @Query("""
            SELECT o FROM Order o
            LEFT JOIN FETCH o.car
            LEFT JOIN FETCH o.user
            LEFT JOIN FETCH o.repairInvoice
            ORDER BY o.createdAt DESC
            """)
    List<Order> findAllWithDetails();

    // Replaces OrderDao.findByUserId() — "user.id" navigation via Spring Data
    @Query("""
            SELECT o FROM Order o
            LEFT JOIN FETCH o.car
            LEFT JOIN FETCH o.user
            LEFT JOIN FETCH o.repairInvoice
            WHERE o.user.id = :userId
            ORDER BY o.createdAt DESC
            """)
    List<Order> findByUserIdWithDetails(@Param("userId") Long userId);

    // Replaces OrderDao.hasConflict() — two date ranges overlap when:
    //   existing.startDate <= newEnd  AND  existing.endDate >= newStart
    @Query("""
            SELECT COUNT(o) > 0 FROM Order o
            WHERE o.car.id = :carId
              AND o.status IN :statuses
              AND o.startDate <= :endDate
              AND o.endDate   >= :startDate
            """)
    boolean existsConflict(@Param("carId") Long carId,
                           @Param("startDate") LocalDate startDate,
                           @Param("endDate") LocalDate endDate,
                           @Param("statuses") List<OrderStatus> statuses);

    // Convenience wrapper that hard-codes the blocking statuses,
    // matching the exact semantics of lab1's OrderDao.hasConflict().
    default boolean hasConflict(Long carId, LocalDate startDate, LocalDate endDate) {
        return existsConflict(carId, startDate, endDate,
                List.of(OrderStatus.PENDING, OrderStatus.PAID, OrderStatus.ACTIVE));
    }
}
