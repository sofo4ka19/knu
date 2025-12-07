package com.example.chef.model;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class IngredientTest {

    @Test
    void testIngredientCreation() {
        Ingredient ing = new Ingredient("Морква", 100.0);
        assertEquals("Морква", ing.getVegetableName());
        assertEquals(100.0, ing.getWeight());
    }

    @Test
    void testInvalidWeight() {
        assertThrows(IllegalArgumentException.class,
                () -> new Ingredient("Морква", 0));
        assertThrows(IllegalArgumentException.class,
                () -> new Ingredient("Морква", -10));
    }

    @Test
    void testSetWeight() {
        Ingredient ing = new Ingredient("Морква", 100.0);
        ing.setWeight(150.0);
        assertEquals(150.0, ing.getWeight());
    }

    @Test
    void testInvalidVegetableName() {
        assertThrows(IllegalArgumentException.class,
                () -> new Ingredient("", 100.0));
        assertThrows(IllegalArgumentException.class,
                () -> new Ingredient(null, 100.0));
    }

    @Test
    void testToFileString() {
        Ingredient ing = new Ingredient("Морква", 100.0);
        assertEquals("Морква;100,00", ing.toFileString());
    }
}