package com.carrental.config;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class DatabaseConfig {

    private static final Logger log = LogManager.getLogger(DatabaseConfig.class);

    private static volatile DatabaseConfig instance;

    private final BlockingQueue<Connection> pool;
    private final String url;
    private final String username;
    private final String password;
    private final int poolSize;

    private DatabaseConfig() {
        Properties props = loadProperties();
        this.url      = props.getProperty("db.url");
        this.username = props.getProperty("db.username");
        this.password = props.getProperty("db.password");
        this.poolSize = Integer.parseInt(props.getProperty("db.pool.size", "10"));

        try {
            Class.forName(props.getProperty("db.driver"));
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("PostgreSQL driver not found", e);
        }

        this.pool = new ArrayBlockingQueue<>(poolSize);
        initPool();
        log.info("Database pool initialized with {} connections", poolSize);
    }

    public static DatabaseConfig getInstance() {
        if (instance == null) {
            synchronized (DatabaseConfig.class) {
                if (instance == null) {
                    instance = new DatabaseConfig();
                }
            }
        }
        return instance;
    }

    private void initPool() {
        for (int i = 0; i < poolSize; i++) {
            try {
                pool.offer(createConnection());
            } catch (SQLException e) {
                throw new RuntimeException("Failed to create DB connection", e);
            }
        }
    }

    private Connection createConnection() throws SQLException {
        return DriverManager.getConnection(url, username, password);
    }

    public Connection getConnection() {
        try {
            Connection conn = pool.take();
            if (conn.isClosed()) {
                log.warn("Connection was closed, creating new one");
                conn = createConnection();
            }
            return conn;
        } catch (InterruptedException | SQLException e) {
            throw new RuntimeException("Failed to get connection from pool", e);
        }
    }

    public void releaseConnection(Connection conn) {
        if (conn != null) {
            pool.offer(conn);
        }
    }

    private Properties loadProperties() {
        Properties props = new Properties();
        try (InputStream is = getClass()
                .getClassLoader()
                .getResourceAsStream("db.properties")) {
            if (is == null) throw new RuntimeException("db.properties not found");
            props.load(is);
        } catch (IOException e) {
            throw new RuntimeException("Cannot load db.properties", e);
        }
        return props;
    }
}