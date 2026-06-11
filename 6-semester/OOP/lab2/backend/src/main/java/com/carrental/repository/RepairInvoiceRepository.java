package com.carrental.repository;

import com.carrental.model.RepairInvoice;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface RepairInvoiceRepository extends JpaRepository<RepairInvoice, Long> {

    // RepairInvoice.order is of type Order, so Spring Data navigates order.id.
    // Replaces RepairInvoiceDao.findByOrderId().
    Optional<RepairInvoice> findByOrderId(Long orderId);

    // save() and findById() inherited from JpaRepository.
    // markAsPaid() from lab1 is replaced by: fetch invoice, invoice.setPaid(true),
    // Hibernate auto-issues UPDATE inside the service transaction.
}
