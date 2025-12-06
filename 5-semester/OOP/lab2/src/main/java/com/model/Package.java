package com.model;

import java.math.BigDecimal; // use this for prices

public class Package {
    private String type;
    private int quantity;
    private BigDecimal price;

    // Getters and Setters
    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    @Override
    public String toString() {
        return "Package{type='" + type + "', price=" + price + "}";
    }
}