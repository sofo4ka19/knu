package com.carrental.repository;

import com.carrental.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    // Replaces UserDao.findByAuth0Id() — used by UserSyncFilter on every request
    Optional<User> findByAuth0Id(String auth0Id);

    // UserDao.saveIfNotExists() is replaced by service-level logic:
    // findByAuth0Id → update existing, or build + save new User entity.
}
