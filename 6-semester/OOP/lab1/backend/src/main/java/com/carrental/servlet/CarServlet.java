package com.carrental.servlet;

import com.carrental.mapper.CarMapper;
import com.carrental.service.CarService;
import com.carrental.util.JsonUtil;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.util.stream.Collectors;

@WebServlet("/api/cars/*")
public class CarServlet extends HttpServlet {

    private final CarService carService = new CarService();

    @Override
    protected void doGet(HttpServletRequest req,
                         HttpServletResponse resp) throws IOException {
        String pathInfo = req.getPathInfo();

        if (pathInfo == null || pathInfo.equals("/")) {
            var cars = carService.getAllCars().stream()
                    .map(CarMapper.INSTANCE::toDto)
                    .collect(Collectors.toList());
            JsonUtil.writeJson(resp, cars);
        } else {
            try {
                Long id = Long.parseLong(pathInfo.substring(1));
                var car = CarMapper.INSTANCE.toDto(carService.getCarById(id));
                JsonUtil.writeJson(resp, car);
            } catch (NumberFormatException e) {
                JsonUtil.writeError(resp, 400, "Invalid car id");
            } catch (IllegalArgumentException e) {
                JsonUtil.writeError(resp, 404, e.getMessage());
            }
        }
    }
}