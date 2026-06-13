package com.carrental.controller;

import com.carrental.dto.OrderResponseDto;
import com.carrental.dto.RepairInvoiceDto;
import com.carrental.mapper.OrderMapper;
import com.carrental.service.OrderService;
import com.carrental.service.RepairService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/admin")
@RequiredArgsConstructor
public class AdminController {

    private final OrderService orderService;
    private final RepairService repairService;
    private final OrderMapper orderMapper;

    @GetMapping
    public List<OrderResponseDto> getAllOrders() {
        return orderService.getAllOrders().stream()
                .map(orderMapper::toDto)
                .toList();
    }

    @PostMapping("/orders/{id}/activate")
    public OrderResponseDto activate(@PathVariable Long id) {
        return orderMapper.toDto(orderService.activateOrder(id));
    }

    @PostMapping("/orders/{id}/return")
    public OrderResponseDto returnCar(@PathVariable Long id) {
        return orderMapper.toDto(orderService.returnCar(id));
    }

    @PostMapping("/orders/{id}/reject")
    public OrderResponseDto reject(@PathVariable Long id,
                                   @RequestBody Map<String, String> body) {
        return orderMapper.toDto(orderService.rejectOrder(id, body.get("reason")));
    }

    @PostMapping("/orders/{id}/complete")
    public OrderResponseDto complete(@PathVariable Long id) {
        return orderMapper.toDto(orderService.completeOrder(id));
    }

    @PostMapping("/orders/{id}/restore")
    public OrderResponseDto restore(@PathVariable Long id) {
        return orderMapper.toDto(orderService.restoreCarAfterRepair(id));
    }

    @PostMapping("/orders/{id}/damage")
    public RepairInvoiceDto damage(@PathVariable Long id,
                                   @RequestBody RepairInvoiceDto dto) {
        return orderMapper.toDto(repairService.createInvoice(id, dto));
    }
}
