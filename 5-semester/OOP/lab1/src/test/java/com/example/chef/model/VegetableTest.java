package com.example.chef.model;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class VegetableTest {

    @Test
    void testRootVegetableCreation() {
        RootVegetable carrot = new RootVegetable("Морква", 41.0, "оранжевий");
        assertEquals("Морква", carrot.getName());
        assertEquals(41.0, carrot.getCaloriesPer100g());
        assertEquals("ROOT", carrot.getType());
        assertEquals("оранжевий", carrot.getColor());
    }

    @Test
    void testLeafVegetableCreation() {
        LeafVegetable lettuce = new LeafVegetable("Салат", 14.0, "зелене листя", true);
        assertEquals("Салат", lettuce.getName());
        assertEquals("LEAF", lettuce.getType());
        assertTrue(lettuce.isCrispy());
    }

    @Test
    void testFruitVegetableCreation() {
        FruitVegetable tomato = new FruitVegetable("Помідор", 20.0, "червоний", true);
        assertEquals("Помідор", tomato.getName());
        assertEquals("FRUIT", tomato.getType());
        assertTrue(tomato.isHasSeed());
    }

    @Test
    void testInvalidName() {
        assertThrows(IllegalArgumentException.class,
                () -> new RootVegetable("", 41.0, "оранжевий"));
        assertThrows(IllegalArgumentException.class,
                () -> new RootVegetable(null, 41.0, "оранжевий"));
    }

    @Test
    void testNegativeCalories() {
        assertThrows(IllegalArgumentException.class,
                () -> new RootVegetable("Морква", -10.0, "оранжевий"));
    }

    @Test
    void testVegetableEquality() {
        RootVegetable carrot1 = new RootVegetable("Морква", 41.0, "оранжевий");
        RootVegetable carrot2 = new RootVegetable("морква", 41.0, "оранжевий");
        assertEquals(carrot1, carrot2); // регістронезалежне порівняння
    }
}