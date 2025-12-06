package com.lab2.tool;

import com.lab2.model.Medicament;

import java.util.Comparator;

public class MedicamentComparator {

    public static final Comparator<Medicament> BY_NAME = Comparator.comparing(
            Medicament::getName, String.CASE_INSENSITIVE_ORDER);

    public static final Comparator<Medicament> BY_PHARM = Comparator.comparing(
            Medicament::getPharm, String.CASE_INSENSITIVE_ORDER);

    public static final Comparator<Medicament> BY_GROUP = Comparator.comparing(Medicament::getGroup);

    public static final Comparator<Medicament> BY_PRICE = Comparator.comparing(m -> {
        if (m.getVersions() == null || m.getVersions().isEmpty() || m.getVersions().get(0).getPack() == null) {
            return java.math.BigDecimal.ZERO;
        }
        return m.getVersions().get(0).getPack().getPrice();
    });

    public static final Comparator<Medicament> BY_GROUP_THEN_NAME_THEN_PHARM = BY_GROUP
            .thenComparing(BY_NAME)
            .thenComparing(BY_PHARM);
}