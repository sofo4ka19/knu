package com.carrental.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Entity
@Table(name = "users")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // auth0_id — the "sub" claim from the JWT, e.g. "auth0|abc123"
    @Column(name = "auth0_id", nullable = false, unique = true, length = 100)
    private String auth0Id;

    @Column(nullable = false, length = 200)
    private String email;

    @Column(name = "full_name", length = 200)
    private String fullName;

    @Builder.Default
    @Column(nullable = false, length = 20)
    private String role = "CLIENT";

    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
}
