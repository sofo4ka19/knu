package com.example.chef.service;

import com.example.chef.model.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

class VegetableServiceTest {
    private VegetableService service;

    @BeforeEach
    void setUp() {
        service = new VegetableService();
    }

    @Test
    void testAddVegetable() {
        RootVegetable carrot = new RootVegetable("Морква", 41.0, "оранжевий");
        assertTrue(service.addVegetable(carrot));
        assertEquals(1, service.getCount());
    }

    @Test
    void testAddDuplicateVegetable() {
        RootVegetable carrot1 = new RootVegetable("Морква", 41.0, "оранжевий");
        RootVegetable carrot2 = new RootVegetable("морква", 45.0, "жовтий");

        assertTrue(service.addVegetable(carrot1));
        assertFalse(service.addVegetable(carrot2)); // дублікат
    }

    @Test
    void testGetVegetable() {
        RootVegetable carrot = new RootVegetable("Морква", 41.0, "оранжевий");
        service.addVegetable(carrot);

        assertNotNull(service.getVegetable("Морква"));
        assertNotNull(service.getVegetable("морква")); // case-insensitive
    }

    @Test
    void testDeleteVegetable() {
        RootVegetable carrot = new RootVegetable("Морква", 41.0, "оранжевий");
        service.addVegetable(carrot);

        assertTrue(service.deleteVegetable("Морква"));
        assertEquals(0, service.getCount());
    }

    @Test
    void testFindByType() {
        service.addVegetable(new RootVegetable("Морква", 41.0, "оранжевий"));
        service.addVegetable(new LeafVegetable("Салат", 14.0, "зелене", true));
        service.addVegetable(new RootVegetable("Буряк", 43.0, "бордовий"));

        List<Vegetable> roots = service.findByType("ROOT");
        assertEquals(2, roots.size());
    }

    @Test
    void testFindByCalorieRange() {
        service.addVegetable(new RootVegetable("Морква", 41.0, "оранжевий"));
        service.addVegetable(new LeafVegetable("Салат", 14.0, "зелене", true));
        service.addVegetable(new RootVegetable("Буряк", 43.0, "бордовий"));

        List<Vegetable> result = service.findByCalorieRange(40.0, 45.0);
        assertEquals(2, result.size());
    }

    @Test
    void testSortByCalories() {
        service.addVegetable(new RootVegetable("Буряк", 43.0, "бордовий"));
        service.addVegetable(new LeafVegetable("Салат", 14.0, "зелене", true));
        service.addVegetable(new RootVegetable("Морква", 41.0, "оранжевий"));

        List<Vegetable> sorted = service.sortByCalories();
        assertEquals("Салат", sorted.get(0).getName());
        assertEquals("Буряк", sorted.get(2).getName());
    }
}