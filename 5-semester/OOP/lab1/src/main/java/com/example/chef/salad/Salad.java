package com.example.chef.salad;

import com.example.chef.vegetables.Vegetable;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Клас що представляє салат з овочів.
 * Демонструє принципи інкапсуляції та агрегації.
 */
public class Salad {
    private String name;
    private List<Vegetable> vegetables;

    /**
     * Конструктор салату.
     *
     * @param name назва салату
     * @throws IllegalArgumentException якщо назва некоректна
     */
    public Salad(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Назва салату не може бути порожньою");
        }
        this.name = name;
        this.vegetables = new ArrayList<>();
    }

    /**
     * Додає овоч до салату.
     *
     * @param vegetable овоч для додавання
     * @throws IllegalArgumentException якщо овоч null
     */
    public void addVegetable(Vegetable vegetable) {
        if (vegetable == null) {
            throw new IllegalArgumentException("Овоч не може бути null");
        }
        vegetables.add(vegetable);
    }

    /**
     * Видаляє овоч з салату.
     *
     * @param vegetable овоч для видалення
     * @return true якщо овоч був видалений
     */
    public boolean removeVegetable(Vegetable vegetable) {
        return vegetables.remove(vegetable);
    }

    /**
     * Очищує салат (видаляє всі овочі).
     */
    public void clear() {
        vegetables.clear();
    }

    /**
     * Обчислює загальну калорійність салату.
     *
     * @return загальна калорійність в ккал
     */
    public double calculateTotalCalories() {
        return vegetables.stream()
                .mapToDouble(Vegetable::getTotalCalories)
                .sum();
    }

    /**
     * Обчислює загальну вагу салату.
     *
     * @return загальна вага в грамах
     */
    public double calculateTotalWeight() {
        return vegetables.stream()
                .mapToDouble(Vegetable::getWeight)
                .sum();
    }

    /**
     * Сортує овочі за назвою.
     *
     * @return відсортований список овочів
     */
    public List<Vegetable> sortByName() {
        return vegetables.stream()
                .sorted(Comparator.comparing(Vegetable::getName))
                .collect(Collectors.toList());
    }

    /**
     * Сортує овочі за вагою.
     *
     * @return відсортований список овочів
     */
    public List<Vegetable> sortByWeight() {
        return vegetables.stream()
                .sorted(Comparator.comparingDouble(Vegetable::getWeight))
                .collect(Collectors.toList());
    }

    /**
     * Сортує овочі за калорійністю на 100г.
     *
     * @return відсортований список овочів
     */
    public List<Vegetable> sortByCalories() {
        return vegetables.stream()
                .sorted(Comparator.comparingDouble(Vegetable::getCaloriesPer100g))
                .collect(Collectors.toList());
    }

    /**
     * Знаходить овочі в заданому діапазоні калорійності (на 100г).
     *
     * @param minCalories мінімальна калорійність
     * @param maxCalories максимальна калорійність
     * @return список овочів у діапазоні
     * @throws IllegalArgumentException якщо діапазон некоректний
     */
    public List<Vegetable> findByCalorieRange(double minCalories, double maxCalories) {
        if (minCalories < 0 || maxCalories < 0) {
            throw new IllegalArgumentException("Калорійність не може бути від'ємною");
        }
        if (minCalories > maxCalories) {
            throw new IllegalArgumentException("Мінімум не може бути більшим за максимум");
        }

        return vegetables.stream()
                .filter(v -> v.getCaloriesPer100g() >= minCalories
                        && v.getCaloriesPer100g() <= maxCalories)
                .collect(Collectors.toList());
    }

    /**
     * Знаходить овочі за типом.
     *
     * @param type тип овочу
     * @return список овочів заданого типу
     */
    public List<Vegetable> findByType(String type) {
        if (type == null || type.trim().isEmpty()) {
            return new ArrayList<>();
        }

        return vegetables.stream()
                .filter(v -> v.getType().equalsIgnoreCase(type.trim()))
                .collect(Collectors.toList());
    }

    /**
     * Повертає незмінну копію списку овочів.
     *
     * @return незмінний список овочів
     */
    public List<Vegetable> getVegetables() {
        return Collections.unmodifiableList(vegetables);
    }

    public String getName() {
        return name;
    }

    public int getVegetableCount() {
        return vegetables.size();
    }

    public boolean isEmpty() {
        return vegetables.isEmpty();
    }

    @Override
    public String toString() {
        if (vegetables.isEmpty()) {
            return String.format("Салат '%s' - порожній", name);
        }

        StringBuilder sb = new StringBuilder();
        sb.append("═══════════════════════════════════════\n");
        sb.append(String.format("  Салат '%s'\n", name));
        sb.append("═══════════════════════════════════════\n");
        sb.append("Інгредієнти:\n");

        for (int i = 0; i < vegetables.size(); i++) {
            sb.append(String.format("  %d. %s\n", i + 1, vegetables.get(i)));
        }

        sb.append("───────────────────────────────────────\n");
        sb.append(String.format("Загальна вага:        %.1f г\n", calculateTotalWeight()));
        sb.append(String.format("Загальна калорійність: %.1f ккал\n", calculateTotalCalories()));
        sb.append("═══════════════════════════════════════\n");

        return sb.toString();
    }
}