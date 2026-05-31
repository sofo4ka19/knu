package com.carrental.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.Map;

public class JwtUtil {

    private static final Logger log = LogManager.getLogger(JwtUtil.class);
    private static final String AUTH0_DOMAIN = "https://dev-378024ihuz3ym3fa.us.auth0.com/api/v2/";
    private static final String AUDIENCE     = "https://car-rental-api";

    private static volatile JwtUtil instance;
    private final HttpClient httpClient;

    private JwtUtil() {
        this.httpClient = HttpClient.newHttpClient();
    }

    public static JwtUtil getInstance() {
        if (instance == null) {
            synchronized (JwtUtil.class) {
                if (instance == null) instance = new JwtUtil();
            }
        }
        return instance;
    }

    public Claims validateAndGetClaims(String token) {
        try {
            return Jwts.parser()
                    .keyLocator(header -> fetchPublicKey(header.get("kid").toString()))
                    .requireIssuer(AUTH0_DOMAIN)
                    .requireAudience(AUDIENCE)
                    .build()
                    .parseSignedClaims(token)
                    .getPayload();
        } catch (Exception e) {
            log.warn("JWT validation failed: {}", e.getMessage());
            throw new SecurityException("Invalid token: " + e.getMessage());
        }
    }

    public String getSubject(String token) {
        return validateAndGetClaims(token).getSubject();
    }

    public boolean hasAdminRole(Claims claims) {
        Object roles = claims.get("https://car-rental-api/roles");
        if (roles instanceof java.util.List<?> list) {
            return list.contains("admin");
        }
        return false;
    }

    private PublicKey fetchPublicKey(String kid) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(AUTH0_DOMAIN + ".well-known/jwks.json"))
                    .GET()
                    .build();
            HttpResponse<String> response = httpClient.send(
                    request, HttpResponse.BodyHandlers.ofString());
            return extractKeyFromJwks(response.body(), kid);
        } catch (Exception e) {
            throw new RuntimeException("Cannot fetch JWKS", e);
        }
    }

    private PublicKey extractKeyFromJwks(String jwksJson, String kid) throws Exception {
        int kidIdx = jwksJson.indexOf("\"" + kid + "\"");
        int nStart = jwksJson.indexOf("\"n\":\"", kidIdx) + 5;
        int nEnd   = jwksJson.indexOf("\"", nStart);
        int eStart = jwksJson.indexOf("\"e\":\"", kidIdx) + 5;
        int eEnd   = jwksJson.indexOf("\"", eStart);

        byte[] modulusBytes  = Base64.getUrlDecoder().decode(jwksJson.substring(nStart, nEnd));
        byte[] exponentBytes = Base64.getUrlDecoder().decode(jwksJson.substring(eStart, eEnd));

        java.security.spec.RSAPublicKeySpec spec = new java.security.spec.RSAPublicKeySpec(
                new java.math.BigInteger(1, modulusBytes),
                new java.math.BigInteger(1, exponentBytes));

        return KeyFactory.getInstance("RSA").generatePublic(spec);
    }
}