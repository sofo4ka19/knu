package com.carrental.controller;

import com.carrental.dto.OrderRequestDto;
import com.carrental.dto.OrderResponseDto;
import com.carrental.mapper.OrderMapper;
import com.carrental.model.User;
import com.carrental.service.OrderService;
import com.carrental.service.RepairService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;
    private final RepairService repairService;
    private final OrderMapper orderMapper;

    @GetMapping("/my")
    public List<OrderResponseDto> getMyOrders(@RequestAttribute("currentUser") User currentUser) {
        return orderService.getMyOrders(currentUser.getId()).stream()
                .map(orderMapper::toDto)
                .toList();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public OrderResponseDto createOrder(@RequestBody OrderRequestDto dto,
                                        @RequestAttribute("currentUser") User currentUser) {
        return orderMapper.toDto(orderService.createOrder(dto, currentUser));
    }

    @PostMapping("/{id}/pay")
    public OrderResponseDto pay(@PathVariable Long id,
                                @RequestAttribute("currentUser") User currentUser) {
        return orderMapper.toDto(orderService.payOrder(id, currentUser.getId()));
    }

    @PostMapping("/{id}/pay-repair")
    public Map<String, Boolean> payRepair(@PathVariable Long id,
                                          @RequestAttribute("currentUser") User currentUser) {
        orderService.verifyOwnerPublic(id, currentUser.getId());
        repairService.payRepair(id);
        return Map.of("success", true);
    }
}
