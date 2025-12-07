package com.example.chef.service;

import com.example.chef.model.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class SaladServiceTest {
    private SaladService saladService;

    @BeforeEach
    void setUp() {
        VegetableService vegService = new VegetableService();
        saladService = new SaladService(vegService);

        // Додаємо тестові овочі
        vegService.addVegetable(new FruitVegetable("Помідор", 20.0, "червоний", true));
        vegService.addVegetable(new LeafVegetable("Салат", 14.0, "зелене", true));
        vegService.addVegetable(new RootVegetable("Цибуля", 40.0, "білий"));
    }

    @Test
    void testCreateSalad() {
        Salad salad = new Salad("Грецький");
        assertTrue(saladService.createSalad(salad));
        assertEquals(1, saladService.getCount());
    }

    @Test
    void testAddIngredient() {
        Salad salad = new Salad("Грецький");
        saladService.createSalad(salad);

        assertTrue(saladService.addIngredient("Грецький", "Помідор", 150.0));
        assertEquals(1, salad.getIngredientCount());
    }

    @Test
    void testCalculateCalories() {
        Salad salad = new Salad("Грецький");
        saladService.createSalad(salad);
        saladService.addIngredient("Грецький", "Помідор", 100.0); // 20 ккал
        saladService.addIngredient("Грецький", "Салат", 100.0);   // 14 ккал

        double calories = saladService.calculateCalories("Грецький");
        assertEquals(34.0, calories, 0.01);
    }

    @Test
    void testCalculateWeight() {
        Salad salad = new Salad("Грецький");
        saladService.createSalad(salad);
        saladService.addIngredient("Грецький", "Помідор", 150.0);
        saladService.addIngredient("Грецький", "Салат", 100.0);

        double weight = saladService.calculateWeight("Грецький");
        assertEquals(250.0, weight);
    }

    @Test
    void testSortIngredientsByWeight() {
        Salad salad = new Salad("Грецький");
        saladService.createSalad(salad);
        saladService.addIngredient("Грецький", "Помідор", 150.0);
        saladService.addIngredient("Грецький", "Салат", 100.0);
        saladService.addIngredient("Грецький", "Цибуля", 200.0);

        List<Ingredient> sorted = saladService.sortIngredientsByWeight("Грецький");
        assertEquals("Салат", sorted.get(0).getVegetableName());
        assertEquals("Цибуля", sorted.get(2).getVegetableName());
    }

    @Test
    void testFindIngredientsByCalorieRange() {
        Salad salad = new Salad("Грецький");
        saladService.createSalad(salad);
        saladService.addIngredient("Грецький", "Помідор", 150.0); // 20 ккал/100г
        saladService.addIngredient("Грецький", "Салат", 100.0);   // 14 ккал/100г
        saladService.addIngredient("Грецький", "Цибуля", 50.0);   // 40 ккал/100г

        List<Ingredient> found = saladService.findIngredientsByCalorieRange("Грецький", 15.0, 25.0);
        assertEquals(1, found.size());
        assertEquals("Помідор", found.get(0).getVegetableName());
    }

    @Test
    void testDeleteSalad() {
        Salad salad = new Salad("Грецький");
        saladService.createSalad(salad);

        assertTrue(saladService.deleteSalad("Грецький"));
        assertEquals(0, saladService.getCount());
    }
}