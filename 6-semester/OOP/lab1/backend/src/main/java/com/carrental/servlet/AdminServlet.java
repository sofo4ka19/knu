package com.carrental.servlet;

import com.carrental.dto.RepairInvoiceDto;
import com.carrental.mapper.OrderMapper;
import com.carrental.service.OrderService;
import com.carrental.service.RepairService;
import com.carrental.util.JsonUtil;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.util.Map;
import java.util.stream.Collectors;

@WebServlet("/api/admin/*")
public class AdminServlet extends HttpServlet {

    private final OrderService  orderService  = new OrderService();
    private final RepairService repairService = new RepairService();

    @Override
    protected void doGet(HttpServletRequest req,
                         HttpServletResponse resp) throws IOException {
        try {
            var orders = orderService.getAllOrders().stream()
                    .map(OrderMapper.INSTANCE::toDto)
                    .collect(Collectors.toList());
            JsonUtil.writeJson(resp, orders);
        } catch (Exception e) {
            JsonUtil.writeError(resp, 500, e.getMessage());
        }
    }

    @Override
    protected void doPost(HttpServletRequest req,
                          HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo(); // "/orders/42/return" тощо

        try {
            if (pathInfo.matches("/orders/\\d+/activate")) {
                Long id = extractOrderId(pathInfo);
                JsonUtil.writeJson(resp,
                        OrderMapper.INSTANCE.toDto(orderService.activateOrder(id)));

            } else if (pathInfo.matches("/orders/\\d+/return")) {
                Long id = extractOrderId(pathInfo);
                JsonUtil.writeJson(resp,
                        OrderMapper.INSTANCE.toDto(orderService.returnCar(id)));

            } else if (pathInfo.matches("/orders/\\d+/reject")) {
                Long id = extractOrderId(pathInfo);
                @SuppressWarnings("unchecked")
                Map<String, String> body = JsonUtil.readBody(req, Map.class);
                JsonUtil.writeJson(resp,
                        OrderMapper.INSTANCE.toDto(
                                orderService.rejectOrder(id, body.get("reason"))));

            } else if (pathInfo.matches("/orders/\\d+/complete")) {
                Long id = extractOrderId(pathInfo);
                JsonUtil.writeJson(resp,
                        OrderMapper.INSTANCE.toDto(orderService.completeOrder(id)));

            } else if (pathInfo.matches("/orders/\\d+/restore")) {
                Long id = extractOrderId(pathInfo);
                JsonUtil.writeJson(resp,
                        OrderMapper.INSTANCE.toDto(orderService.restoreCarAfterRepair(id)));

            } else if (pathInfo.matches("/orders/\\d+/damage")) {
                Long id = extractOrderId(pathInfo);
                RepairInvoiceDto dto = JsonUtil.readBody(req, RepairInvoiceDto.class);
                JsonUtil.writeJson(resp, repairService.createInvoice(id, dto));

            } else {
                JsonUtil.writeError(resp, 404, "Admin endpoint not found");
            }
        } catch (IllegalArgumentException e) {
            JsonUtil.writeError(resp, 400, e.getMessage());
        } catch (IllegalStateException e) {
            JsonUtil.writeError(resp, 409, e.getMessage());
        }
    }

    private Long extractOrderId(String pathInfo) {
        // "/orders/42/return" -> 42
        return Long.parseLong(pathInfo.split("/")[2]);
    }
}