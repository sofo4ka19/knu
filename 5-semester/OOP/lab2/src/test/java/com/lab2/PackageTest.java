package com.lab2;

import com.lab2.model.Package;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.junit.jupiter.api.Assertions.*;

class PackageTest {

    @Test
    void testPricePrecision() {
        Package pack = new Package();
        BigDecimal price = new BigDecimal("145.55");

        pack.setPrice(price);

        assertEquals(new BigDecimal("145.55"), pack.getPrice());
        assertNotEquals(new BigDecimal("145.5"), pack.getPrice());
    }

    @Test
    void testPackageQuantityPositive() {
        Package pack = new Package();
        pack.setQuantity(10);
        assertTrue(pack.getQuantity() > 0, "Quantity should be positive");
    }
}
