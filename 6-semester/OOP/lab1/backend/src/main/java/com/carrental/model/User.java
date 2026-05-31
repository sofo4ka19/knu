package com.carrental.model;

import lombok.*;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    private Long id;
    private String auth0Id;
    private String email;
    private String fullName;

    @Builder.Default
    private String role = "CLIENT";

    private LocalDateTime createdAt;
}