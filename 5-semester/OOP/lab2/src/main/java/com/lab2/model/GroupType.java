package com.lab2.model;

public enum GroupType {
    ANTIBIOTICS,
    PAINKILLERS,
    VITAMINS,
    SEDATIVES,
    ANTIVIRAL;

    public static GroupType fromValue(String v) {
        return valueOf(v);
    }
}
