package com.example.chef.model;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class SaladTest {
    private Salad salad;

    @BeforeEach
    void setUp() {
        salad = new Salad("Грецький салат");
    }

    @Test
    void testSaladCreation() {
        assertEquals("Грецький салат", salad.getName());
        assertTrue(salad.isEmpty());
        assertEquals(0, salad.getIngredientCount());
    }

    @Test
    void testInvalidName() {
        assertThrows(IllegalArgumentException.class, () -> new Salad(""));
        assertThrows(IllegalArgumentException.class, () -> new Salad(null));
    }

    @Test
    void testAddIngredient() {
        salad.addIngredient("Помідор", 150.0);
        assertEquals(1, salad.getIngredientCount());
        assertFalse(salad.isEmpty());
        assertTrue(salad.hasIngredient("Помідор"));
    }

    @Test
    void testRemoveIngredientByIndex() {
        salad.addIngredient("Помідор", 150.0);
        salad.addIngredient("Огірок", 100.0);

        assertTrue(salad.removeIngredient(0));
        assertEquals(1, salad.getIngredientCount());
        assertFalse(salad.hasIngredient("Помідор"));
    }

    @Test
    void testRemoveIngredientByName() {
        salad.addIngredient("Помідор", 150.0);

        assertTrue(salad.removeIngredient("Помідор"));
        assertTrue(salad.isEmpty());
    }

    @Test
    void testUpdateWeight() {
        salad.addIngredient("Помідор", 150.0);

        assertTrue(salad.updateWeight("Помідор", 200.0));
        assertEquals(200.0, salad.getIngredients().get(0).getWeight());
    }

    @Test
    void testClear() {
        salad.addIngredient("Помідор", 150.0);
        salad.addIngredient("Огірок", 100.0);

        salad.clear();
        assertTrue(salad.isEmpty());
    }
}