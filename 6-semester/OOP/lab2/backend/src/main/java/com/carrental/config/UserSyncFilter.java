package com.carrental.config;

import com.carrental.model.User;
import com.carrental.repository.UserRepository;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

@Component
@RequiredArgsConstructor
public class UserSyncFilter extends OncePerRequestFilter {

    private final UserRepository userRepository;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();

        if (auth instanceof JwtAuthenticationToken jwtAuth) {
            Jwt jwt = jwtAuth.getToken();
            String auth0Id = jwt.getSubject();

            User user = userRepository.findByAuth0Id(auth0Id).orElseGet(() -> {
                String email = jwt.getClaimAsString("email");
                String name  = jwt.getClaimAsString("name");
                return userRepository.save(User.builder()
                        .auth0Id(auth0Id)
                        .email(email != null ? email : auth0Id + "@placeholder.com")
                        .fullName(name != null ? name : auth0Id)
                        .role("CLIENT")
                        .build());
            });

            request.setAttribute("currentUser", user);
        }

        filterChain.doFilter(request, response);
    }
}
