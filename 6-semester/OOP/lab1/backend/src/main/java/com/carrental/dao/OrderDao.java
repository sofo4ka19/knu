package com.carrental.dao;

import com.carrental.config.DatabaseConfig;
import com.carrental.model.Order;
import com.carrental.model.enums.OrderStatus;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class OrderDao {

    private static final Logger log = LogManager.getLogger(OrderDao.class);
    private final DatabaseConfig db = DatabaseConfig.getInstance();
    private final CarDao carDao = new CarDao();
    private final UserDao userDao = new UserDao();

    private Order mapRow(ResultSet rs) throws SQLException {
        Long carId  = rs.getLong("car_id");
        Long userId = rs.getLong("user_id");

        return Order.builder()
                .id(rs.getLong("id"))
                .car(carDao.findById(carId).orElse(null))
                .user(userDao.findById(userId).orElse(null))
                .passportData(rs.getString("passport_data"))
                .startDate(rs.getDate("start_date").toLocalDate())
                .endDate(rs.getDate("end_date").toLocalDate())
                .totalPrice(rs.getBigDecimal("total_price"))
                .status(OrderStatus.valueOf(rs.getString("status")))
                .rejectionReason(rs.getString("rejection_reason"))
                .createdAt(rs.getTimestamp("created_at").toLocalDateTime())
                .build();
    }

    // Return id of the created row
    public Order save(Order order) {
        String sql = """
                INSERT INTO orders
                    (car_id, user_id, passport_data, start_date, end_date,
                     total_price, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, NOW())
                """;
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(
                sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setLong(1,   order.getCar().getId());
            ps.setLong(2,   order.getUser().getId());
            ps.setString(3, order.getPassportData());
            ps.setDate(4,   Date.valueOf(order.getStartDate()));
            ps.setDate(5,   Date.valueOf(order.getEndDate()));
            ps.setBigDecimal(6, order.getTotalPrice());
            ps.setString(7, order.getStatus().name());
            ps.executeUpdate();

            try (ResultSet keys = ps.getGeneratedKeys()) {
                if (keys.next()) {
                    order.setId(keys.getLong(1));
                }
            }
            log.info("Order created with id {}", order.getId());
            return order;
        } catch (SQLException e) {
            log.error("Error saving order", e);
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
    }

    public void updateStatus(Long orderId, OrderStatus status,
                             String rejectionReason) {
        String sql = """
                UPDATE orders
                SET status = ?, rejection_reason = ?
                WHERE id = ?
                """;
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, status.name());
            ps.setString(2, rejectionReason); // null якщо не відхилено
            ps.setLong(3,   orderId);
            ps.executeUpdate();
        } catch (SQLException e) {
            log.error("Error updating order {} status", orderId, e);
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
    }

    public Optional<Order> findById(Long id) {
        String sql = "SELECT * FROM orders WHERE id = ?";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) return Optional.of(mapRow(rs));
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
        return Optional.empty();
    }

    public List<Order> findByUserId(Long userId) {
        List<Order> orders = new ArrayList<>();
        String sql = "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, userId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) orders.add(mapRow(rs));
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
        return orders;
    }

    // Two date ranges overlap when: existing.start_date <= newEnd AND existing.end_date >= newStart
    public boolean hasConflict(Long carId, LocalDate startDate, LocalDate endDate) {
        String sql = """
                SELECT COUNT(*) FROM orders
                WHERE car_id = ?
                  AND status IN ('PENDING', 'PAID', 'ACTIVE')
                  AND start_date <= ?
                  AND end_date   >= ?
                """;
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1,  carId);
            ps.setDate(2,  Date.valueOf(endDate));
            ps.setDate(3,  Date.valueOf(startDate));
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() && rs.getInt(1) > 0;
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
    }

    public List<Order> findAll() {
        List<Order> orders = new ArrayList<>();
        String sql = "SELECT * FROM orders ORDER BY created_at DESC";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) orders.add(mapRow(rs));
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
        return orders;
    }
}