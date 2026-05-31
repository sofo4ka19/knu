package com.carrental.dao;

import com.carrental.config.DatabaseConfig;
import com.carrental.model.Car;
import com.carrental.model.enums.CarStatus;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class CarDao {

    private static final Logger log = LogManager.getLogger(CarDao.class);
    private final DatabaseConfig db = DatabaseConfig.getInstance();

    private Car mapRow(ResultSet rs) throws SQLException {
        return Car.builder()
                .id(rs.getLong("id"))
                .brand(rs.getString("brand"))
                .model(rs.getString("model"))
                .year(rs.getInt("year"))
                .plateNumber(rs.getString("plate_number"))
                .pricePerDay(rs.getBigDecimal("price_per_day"))
                .status(CarStatus.valueOf(rs.getString("status")))
                .imageUrl(rs.getString("image_url"))
                .createdAt(rs.getTimestamp("created_at").toLocalDateTime())
                .build();
    }

    public List<Car> findAll() {
        List<Car> cars = new ArrayList<>();
        String sql = "SELECT * FROM cars ORDER BY brand, model";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                cars.add(mapRow(rs));
            }
        } catch (SQLException e) {
            log.error("Error fetching all cars", e);
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
        return cars;
    }

    public List<Car> findByStatus(CarStatus status) {
        List<Car> cars = new ArrayList<>();
        String sql = "SELECT * FROM cars WHERE status = ? ORDER BY brand";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, status.name());
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) cars.add(mapRow(rs));
            }
        } catch (SQLException e) {
            log.error("Error fetching cars by status {}", status, e);
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
        return cars;
    }

    public Optional<Car> findById(Long id) {
        String sql = "SELECT * FROM cars WHERE id = ?";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setLong(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) return Optional.of(mapRow(rs));
            }
        } catch (SQLException e) {
            log.error("Error fetching car by id {}", id, e);
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
        return Optional.empty();
    }

    public void updateStatus(Long carId, CarStatus newStatus) {
        String sql = "UPDATE cars SET status = ? WHERE id = ?";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, newStatus.name());
            ps.setLong(2, carId);
            ps.executeUpdate();
            log.debug("Car {} status updated to {}", carId, newStatus);
        } catch (SQLException e) {
            log.error("Error updating car {} status", carId, e);
            throw new RuntimeException(e);
        } finally {
            db.releaseConnection(conn);
        }
    }
}