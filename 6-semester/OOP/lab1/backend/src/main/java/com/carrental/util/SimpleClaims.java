package com.carrental.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ClaimsMutator;

import java.util.*;

// Проста реалізація Claims без залежності від внутрішніх класів JJWT
public class SimpleClaims extends LinkedHashMap<String, Object> implements Claims {

    @Override
    public String getSubject() {
        return (String) get(Claims.SUBJECT);
    }

    @Override
    public String getIssuer() {
        return (String) get(Claims.ISSUER);
    }

    @Override
    public String getId() {
        return (String) get(Claims.ID);
    }

    @Override
    public Date getExpiration() {
        Object exp = get(Claims.EXPIRATION);
        if (exp instanceof Long l) return new Date(l * 1000);
        return null;
    }

    @Override
    public Date getIssuedAt() {
        Object iat = get(Claims.ISSUED_AT);
        if (iat instanceof Long l) return new Date(l * 1000);
        return null;
    }

    @Override
    public Date getNotBefore() {
        Object nbf = get(Claims.NOT_BEFORE);
        if (nbf instanceof Long l) return new Date(l * 1000);
        return null;
    }

    @Override
    public Set<String> getAudience() {
        Object aud = get(Claims.AUDIENCE);
        if (aud instanceof String s) {
            return Set.of(s);
        }
        if (aud instanceof List<?> list) {
            Set<String> result = new LinkedHashSet<>();
            list.forEach(v -> result.add(v.toString()));
            return result;
        }
        return Set.of();
    }

    @Override
    public <T> T get(String claimName, Class<T> requiredType) {
        Object value = get(claimName);
        if (value == null) return null;
        if (requiredType.isInstance(value)) return requiredType.cast(value);
        return null;
    }

}