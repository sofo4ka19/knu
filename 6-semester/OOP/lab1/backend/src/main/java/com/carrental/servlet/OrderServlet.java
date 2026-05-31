package com.carrental.servlet;

import com.carrental.dto.OrderRequestDto;
import com.carrental.mapper.OrderMapper;
import com.carrental.model.User;
import com.carrental.service.OrderService;
import com.carrental.util.JsonUtil;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.util.stream.Collectors;

@WebServlet("/api/orders/*")
public class OrderServlet extends HttpServlet {

    private final OrderService orderService = new OrderService();

    @Override
    protected void doGet(HttpServletRequest req,
                         HttpServletResponse resp) throws IOException {
        // GET /api/orders/my — current user's order
        User currentUser = (User) req.getAttribute("currentUser");
        var orders = orderService.getMyOrders(currentUser.getId()).stream()
                .map(OrderMapper.INSTANCE::toDto)
                .collect(Collectors.toList());
        JsonUtil.writeJson(resp, orders);
    }

    @Override
    protected void doPost(HttpServletRequest req,
                          HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo(); // null, "/42/pay"

        User currentUser = (User) req.getAttribute("currentUser");

        try {
            if (pathInfo == null || pathInfo.equals("/")) {
                // POST /api/orders — create an order
                OrderRequestDto dto = JsonUtil.readBody(req, OrderRequestDto.class);
                var order = orderService.createOrder(dto, currentUser);
                resp.setStatus(HttpServletResponse.SC_CREATED);
                JsonUtil.writeJson(resp, OrderMapper.INSTANCE.toDto(order));

            } else if (pathInfo.matches("/\\d+/pay")) {
                // POST /api/orders/42/pay — pay
                Long orderId = extractId(pathInfo);
                var order = orderService.payOrder(orderId, currentUser.getId());
                JsonUtil.writeJson(resp, OrderMapper.INSTANCE.toDto(order));

            } else {
                JsonUtil.writeError(resp, 404, "Not found");
            }
        } catch (IllegalArgumentException e) {
            JsonUtil.writeError(resp, 400, e.getMessage());
        } catch (IllegalStateException e) {
            JsonUtil.writeError(resp, 409, e.getMessage());
        } catch (SecurityException e) {
            JsonUtil.writeError(resp, 403, e.getMessage());
        }
    }

    private Long extractId(String pathInfo) {
        return Long.parseLong(pathInfo.split("/")[1]);
    }
}