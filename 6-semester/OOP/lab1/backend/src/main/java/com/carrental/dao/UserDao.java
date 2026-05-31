package com.carrental.dao;

import com.carrental.config.DatabaseConfig;
import com.carrental.model.User;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.sql.*;
import java.util.Optional;

public class UserDao {

    private static final Logger log = LogManager.getLogger(UserDao.class);
    private final DatabaseConfig db = DatabaseConfig.getInstance();

    private User mapRow(ResultSet rs) throws SQLException {
        return User.builder()
                .id(rs.getLong("id"))
                .auth0Id(rs.getString("auth0_id"))
                .email(rs.getString("email"))
                .fullName(rs.getString("full_name"))
                .role(rs.getString("role"))
                .createdAt(rs.getTimestamp("created_at").toLocalDateTime())
                .build();
    }

    public Optional<User> findByAuth0Id(String auth0Id) {
        String sql = "SELECT * FROM users WHERE auth0_id = ?";
        Connection conn = db.getConnection();
        try (PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, auth0Id);
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

    public Optional<User> findById(Long id) {
        String sql = "SELECT * FROM users WHERE id = ?";
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

    // During the first login using Auth0 — automatically create new row in DB
    public User saveIfNotExists(String auth0Id, String email, String fullName) {
        return findByAuth0Id(auth0Id).orElseGet(() -> {
            String sql = """
                    INSERT INTO users (auth0_id, email, full_name, role, created_at)
                    VALUES (?, ?, ?, 'CLIENT', NOW())
                    """;
            Connection conn = db.getConnection();
            try (PreparedStatement ps = conn.prepareStatement(
                    sql, Statement.RETURN_GENERATED_KEYS)) {
                ps.setString(1, auth0Id);
                ps.setString(2, email);
                ps.setString(3, fullName);
                ps.executeUpdate();
                try (ResultSet keys = ps.getGeneratedKeys()) {
                    if (keys.next()) {
                        long newId = keys.getLong(1);
                        log.info("New user created: {}, id={}", email, newId);
                        return findById(newId).orElseThrow();
                    }
                }
            } catch (SQLException e) {
                throw new RuntimeException(e);
            } finally {
                db.releaseConnection(conn);
            }
            throw new RuntimeException("Failed to create user");
        });
    }
}