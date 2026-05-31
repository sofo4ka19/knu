package com.carrental.filter;

import com.carrental.util.JsonUtil;
import jakarta.servlet.*;
import jakarta.servlet.annotation.WebFilter;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

// only for admins
@WebFilter("/api/admin/*")
public class RoleFilter implements Filter {

    @Override
    public void doFilter(ServletRequest req, ServletResponse res,
                         FilterChain chain) throws IOException, ServletException {
        HttpServletRequest  request  = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        Boolean isAdmin = (Boolean) request.getAttribute("isAdmin");
        if (!Boolean.TRUE.equals(isAdmin)) {
            JsonUtil.writeError(response, 403, "Admin access required");
            return;
        }

        chain.doFilter(req, res);
    }
}