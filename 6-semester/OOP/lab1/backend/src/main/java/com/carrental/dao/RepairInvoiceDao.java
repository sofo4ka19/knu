package com.carrental.dao;

import com.carrental.config.DatabaseConfig;
import com.carrental.model.RepairInvoice;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.*;
import java.util.Optional;

public class RepairInvoiceDao {

    private static final Logger log = LogManager.getLogger(RepairInvoiceDao.class);
    private final DatabaseConfig db = DatabaseConfig.getInstance();

    public RepairInvoice save(RepairInvoice invoice) {
        String sql = """
                INSERT INTO repair_invoices
                    (order_id, damage_description, repair_cost, created_at)
                VALUES (?, ?, ?, NOW())
                """;
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(
                sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setLong(1,       invoice.getOrderId());
            ps.setString(2,     invoice.getDamageDescription());
            ps.setBigDecimal(3, invoice.getRepairCost());
            ps.executeUpdate();
            try (ResultSet keys = ps.getGeneratedKeys()) {
                if (keys.next()) invoice.setId(keys.getLong(1));
            }
            return invoice;
        } catch (SQLException e) {
            log.error("Error saving repair invoice for order {}", invoice.getOrderId(), e);
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
    }

    public Optional<RepairInvoice> findByOrderId(Long orderId) {
        String sql = "SELECT * FROM repair_invoices WHERE order_id = ?";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, orderId);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return Optional.of(RepairInvoice.builder()
                            .id(rs.getLong("id"))
                            .orderId(rs.getLong("order_id"))
                            .damageDescription(rs.getString("damage_description"))
                            .repairCost(rs.getBigDecimal("repair_cost"))
                            .createdAt(rs.getTimestamp("created_at").toLocalDateTime())
                            .build());
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
        return Optional.empty();
    }
}