package com.lab2;

import com.lab2.model.GroupType;
import com.lab2.model.Medicament;
import com.lab2.tool.MedicamentComparator;

import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class MedicamentComparatorTest {

    @Test
    void testSortingLogic() {
        Medicament m1 = create("B_Name", "Pharm1", GroupType.ANTIBIOTICS);
        Medicament m2 = create("A_Name", "Pharm1", GroupType.ANTIBIOTICS);
        Medicament m3 = create("C_Name", "Pharm1", GroupType.VITAMINS);

        List<Medicament> list = new ArrayList<>();
        list.add(m1);
        list.add(m2);
        list.add(m3);

        list.sort(MedicamentComparator.BY_GROUP_THEN_NAME_THEN_PHARM);

        assertEquals(m2, list.get(0), "First: A_Name (Antibiotics)");
        assertEquals(m1, list.get(1), "Second: B_Name (Antibiotics)");
        assertEquals(m3, list.get(2), "Third: Vitamins");
    }

    private Medicament create(String name, String pharm, GroupType group) {
        Medicament m = new Medicament();
        m.setName(name);
        m.setPharm(pharm);
        m.setGroup(group);
        return m;
    }

    @Test
    void testSortByPrice() {
        Medicament m1 = createWithPrice(new java.math.BigDecimal("100.50"));
        Medicament m2 = createWithPrice(new java.math.BigDecimal("50.00"));
        Medicament m3 = createWithPrice(new java.math.BigDecimal("500.00"));

        List<Medicament> list = new ArrayList<>();
        list.add(m1);
        list.add(m2);
        list.add(m3);

        list.sort(MedicamentComparator.BY_PRICE);

        assertEquals(m2, list.get(0), "50.00 should be first");
        assertEquals(m1, list.get(1), "100.50 should be second");
        assertEquals(m3, list.get(2), "500.00 should be last");
    }

    @Test
    void testCaseInsensitivity() {
        Medicament m1 = create("alpha", "Ph", GroupType.VITAMINS);
        Medicament m2 = create("Beta", "Ph", GroupType.VITAMINS);

        List<Medicament> list = new ArrayList<>();
        list.add(m2);
        list.add(m1);

        list.sort(MedicamentComparator.BY_NAME);

        assertEquals(m1, list.get(0), "'alpha' should come before 'Beta'");
    }

    private Medicament createWithPrice(java.math.BigDecimal price) {
        Medicament m = new Medicament();
        com.lab2.model.Version v = new com.lab2.model.Version();
        com.lab2.model.Package p = new com.lab2.model.Package();
        p.setPrice(price);
        v.setPack(p);

        List<com.lab2.model.Version> versions = new ArrayList<>();
        versions.add(v);
        m.setVersions(versions);
        return m;
    }
}