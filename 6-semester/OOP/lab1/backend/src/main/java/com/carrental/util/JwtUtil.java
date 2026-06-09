package com.carrental.util;

import com.carrental.util.SimpleClaims;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.jsonwebtoken.Claims;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.ByteArrayInputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.PublicKey;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

public class JwtUtil {

    private static final Logger log = LogManager.getLogger(JwtUtil.class);

    private static final String AUTH0_DOMAIN =
            "https://dev-378024ihuz3ym3fa.us.auth0.com/";
    private static final String AUDIENCE = "https://car-rental-api";
    private static final String JWKS_URL =
            AUTH0_DOMAIN + ".well-known/jwks.json";

    private static volatile JwtUtil instance;
    private final HttpClient httpClient;
    private final Map<String, PublicKey> keyCache = new ConcurrentHashMap<>();
    private final ObjectMapper mapper = new ObjectMapper();

    private JwtUtil() {
        this.httpClient = HttpClient.newHttpClient();
        preloadKeys();
    }

    public static JwtUtil getInstance() {
        if (instance == null) {
            synchronized (JwtUtil.class) {
                if (instance == null) instance = new JwtUtil();
            }
        }
        return instance;
    }

    private void preloadKeys() {
        try {
            String jwks = fetchJwks();
            parseAndCacheKeys(jwks);
            log.info("Loaded {} public keys from Auth0 JWKS", keyCache.size());
            keyCache.keySet().forEach(kid -> log.info("Cached key kid: {}", kid));
        } catch (Exception e) {
            log.error("Failed to preload JWKS keys: {}", e.getMessage(), e);
        }
    }

    private String fetchJwks() throws Exception {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(JWKS_URL))
                .GET()
                .build();
        HttpResponse<String> response = httpClient.send(
                request, HttpResponse.BodyHandlers.ofString());
        log.debug("JWKS response status: {}", response.statusCode());
        return response.body();
    }

    private void parseAndCacheKeys(String jwksJson) throws Exception {
        JsonNode keys = mapper.readTree(jwksJson).get("keys");

        for (JsonNode key : keys) {
            String kid = key.get("kid").asText();
            String kty = key.get("kty").asText();
            if (!"RSA".equals(kty)) continue;

            try {
                // x5c — готовий X.509 сертифікат від Auth0
                // надійніше ніж вручну будувати з n і e
                String x5c = key.get("x5c").get(0).asText();
                byte[] certBytes = Base64.getDecoder().decode(x5c);

                CertificateFactory cf = CertificateFactory.getInstance("X.509");
                X509Certificate cert = (X509Certificate) cf.generateCertificate(
                        new ByteArrayInputStream(certBytes));

                PublicKey publicKey = cert.getPublicKey();
                keyCache.put(kid, publicKey);

                log.info("Cached x5c key for kid: {}, algorithm: {}",
                        kid, publicKey.getAlgorithm());
                log.debug("Public key encoded: {}",
                        Base64.getEncoder().encodeToString(publicKey.getEncoded()));

            } catch (Exception ex) {
                log.warn("Failed to load x5c for kid {}: {}", kid, ex.getMessage());
            }
        }
    }

    public Claims validateAndGetClaims(String token) {
        try {
            String[] parts = token.split("\\.");
            if (parts.length != 3) {
                throw new SecurityException("Invalid JWT format");
            }

            // Декодуємо header
            String headerJson = new String(
                    Base64.getUrlDecoder().decode(addPadding(parts[0])),
                    StandardCharsets.UTF_8);
            log.debug("Token header: {}", headerJson);

            // Витягуємо kid
            JsonNode header = mapper.readTree(headerJson);
            String kid = header.get("kid").asText();
            log.debug("Token kid: {}", kid);

            // Знаходимо ключ
            PublicKey publicKey = keyCache.get(kid);
            if (publicKey == null) {
                log.warn("Key not found for kid: {}, reloading JWKS", kid);
                parseAndCacheKeys(fetchJwks());
                publicKey = keyCache.get(kid);
            }
            if (publicKey == null) {
                throw new SecurityException("No key found for kid: " + kid);
            }

            // Перевіряємо підпис через стандартний Java Signature
            String signingInput = parts[0] + "." + parts[1];
            byte[] signatureBytes = Base64.getUrlDecoder()
                    .decode(addPadding(parts[2]));

            java.security.Signature sig =
                    java.security.Signature.getInstance("SHA256withRSA");
            sig.initVerify(publicKey);
            sig.update(signingInput.getBytes(StandardCharsets.UTF_8));
            boolean valid = sig.verify(signatureBytes);

            if (!valid) {
                throw new SecurityException("Signature verification failed");
            }

            log.debug("Signature verified successfully");

            // Декодуємо payload
            String payloadJson = new String(
                    Base64.getUrlDecoder().decode(addPadding(parts[1])),
                    StandardCharsets.UTF_8);
            log.debug("Token payload: {}", payloadJson);

            JsonNode payloadNode = mapper.readTree(payloadJson);

            // Перевіряємо expiration
            long exp = payloadNode.get("exp").asLong();
            long now = System.currentTimeMillis() / 1000;
            if (now > exp) {
                throw new SecurityException("Token expired");
            }

            // Перевіряємо issuer
            String iss = payloadNode.get("iss").asText();
            if (!AUTH0_DOMAIN.equals(iss)) {
                log.warn("Invalid issuer: {}", iss);
                throw new SecurityException("Invalid issuer");
            }

            // Перевіряємо audience
            JsonNode audNode = payloadNode.get("aud");
            boolean audValid = false;
            if (audNode != null && audNode.isArray()) {
                for (JsonNode a : audNode) {
                    if (AUDIENCE.equals(a.asText())) {
                        audValid = true;
                        break;
                    }
                }
            } else if (audNode != null) {
                audValid = AUDIENCE.equals(audNode.asText());
            }

            if (!audValid) {
                log.warn("Invalid audience: {}", audNode);
                throw new SecurityException("Invalid audience");
            }

            // Будуємо Claims
            SimpleClaims claims = new SimpleClaims();
            payloadNode.fields().forEachRemaining(entry -> {
                JsonNode value = entry.getValue();
                if (value.isTextual()) {
                    claims.put(entry.getKey(), value.asText());
                } else if (value.isLong() || value.isInt()) {
                    claims.put(entry.getKey(), value.asLong());
                } else if (value.isArray()) {
                    List<String> list = new ArrayList<>();
                    value.forEach(v -> list.add(v.asText()));
                    claims.put(entry.getKey(), list);
                } else {
                    claims.put(entry.getKey(), value.asText());
                }
            });

            log.debug("Token valid for sub: {}", claims.getSubject());
            return claims;

        } catch (SecurityException e) {
            throw e;
        } catch (Exception e) {
            log.warn("JWT validation failed: {}", e.getMessage(), e);
            throw new SecurityException("Invalid token: " + e.getMessage());
        }
    }

    public String getSubject(String token) {
        return validateAndGetClaims(token).getSubject();
    }

    public boolean hasAdminRole(Claims claims) {
        Object roles = claims.get("https://car-rental-api/roles");
        if (roles instanceof List<?> list) {
            return list.contains("admin");
        }
        return false;
    }

    // Base64URL може не мати padding — Java декодер його вимагає
    private String addPadding(String base64url) {
        int remainder = base64url.length() % 4;
        if (remainder == 2) return base64url + "==";
        if (remainder == 3) return base64url + "=";
        return base64url;
    }
}