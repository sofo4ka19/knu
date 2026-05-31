package com.carrental.filter;

import com.carrental.dao.UserDao;
import com.carrental.model.User;
import com.carrental.util.JsonUtil;
import com.carrental.util.JwtUtil;
import io.jsonwebtoken.Claims;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebFilter;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;

@WebFilter("/api/*")
public class AuthFilter implements Filter {

    private static final Logger log = LogManager.getLogger(AuthFilter.class);
    private final JwtUtil jwtUtil = JwtUtil.getInstance();
    private final UserDao userDao = new UserDao();

    private static final java.util.Set<String> PUBLIC_PATHS = java.util.Set.of(
            "/api/cars"
    );

    @Override
    public void doFilter(ServletRequest req, ServletResponse res,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest  request  = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        String path   = request.getServletPath();
        String method = request.getMethod();

        if ("GET".equals(method) && PUBLIC_PATHS.contains(path)) {
            chain.doFilter(req, res);
            return;
        }

        String authHeader = request.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            JsonUtil.writeError(response, 401, "Authorization header missing");
            return;
        }

        String token = authHeader.substring(7);

        try {
            Claims claims = jwtUtil.validateAndGetClaims(token);
            String auth0Id = claims.getSubject();
            String email   = claims.get("email", String.class);
            String name    = claims.get("name", String.class);

            User user = userDao.saveIfNotExists(auth0Id, email, name);

            request.setAttribute("currentUser",   user);
            request.setAttribute("jwtClaims",     claims);
            request.setAttribute("isAdmin",
                    jwtUtil.hasAdminRole(claims) || "ADMIN".equals(user.getRole()));

            log.debug("Authenticated user: {}", email);
            chain.doFilter(req, res);

        } catch (SecurityException e) {
            log.warn("Auth failed for {}: {}", path, e.getMessage());
            JsonUtil.writeError(response, 401, "Invalid token");
        }
    }
}