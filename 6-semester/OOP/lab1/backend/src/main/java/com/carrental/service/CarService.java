package com.carrental.service;

import com.carrental.dao.CarDao;
import com.carrental.model.Car;
import com.carrental.model.enums.CarStatus;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.List;

public class CarService {

    private static final Logger log = LogManager.getLogger(CarService.class);
    private final CarDao carDao;

    public CarService() {
        this.carDao = new CarDao();
    }

    public CarService(CarDao carDao) {
        this.carDao = carDao;
    }

    public List<Car> getAvailableCars() {
        log.debug("Fetching available cars");
        return carDao.findByStatus(CarStatus.AVAILABLE);
    }

    public Car getCarById(Long id) {
        return carDao.findById(id)
                .orElseThrow(() -> new IllegalArgumentException(
                        "Car not found: " + id));
    }

    public List<Car> getAllCars() {
        return carDao.findAll();
    }
}