package com.carrental.repository;

import com.carrental.model.Car;
import com.carrental.model.enums.CarStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CarRepository extends JpaRepository<Car, Long> {

    // Replaces CarDao.findAll() — ORDER BY brand, model
    List<Car> findAllByOrderByBrandAscModelAsc();

    // Replaces CarDao.findByStatus() — ORDER BY brand
    List<Car> findByStatusOrderByBrand(CarStatus status);

    // findById(Long) and save(Car) are inherited from JpaRepository.
    // updateStatus() from lab1 has no repository method — the service
    // fetches the entity, calls car.setStatus(), and Hibernate issues
    // the UPDATE automatically at the end of the transaction.
}
