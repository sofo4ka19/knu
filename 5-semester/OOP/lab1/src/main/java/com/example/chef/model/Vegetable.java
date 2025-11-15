package com.example.chef.model;

import java.util.Objects;

public abstract class Vegetable {
    private String name;
    private double caloriesPer100g;

    public Vegetable(String name, double caloriesPer100g) {
        validateName(name);
        validateCalories(caloriesPer100g);
        this.name = name;
        this.caloriesPer100g = caloriesPer100g;
    }

    private void validateName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Назва не може бути порожньою");
        }
    }

    private void validateCalories(double calories) {
        if (calories < 0) {
            throw new IllegalArgumentException("Калорійність не може бути від'ємною");
        }
    }

    public abstract String getType();
    public abstract String toFileString(); // для збереження

    public String getName() { return name; }
    public double getCaloriesPer100g() { return caloriesPer100g; }

    public void setName(String name) {
        validateName(name);
        this.name = name;
    }

    public void setCaloriesPer100g(double caloriesPer100g) {
        validateCalories(caloriesPer100g);
        this.caloriesPer100g = caloriesPer100g;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Vegetable vegetable = (Vegetable) o;
        return Objects.equals(name.toLowerCase(), vegetable.name.toLowerCase());
    }

    @Override
    public int hashCode() {
        return Objects.hash(name.toLowerCase());
    }

    @Override
    public String toString() {
        return String.format("%s (%s) - %.1f ккал/100г", name, getType(), caloriesPer100g);
    }
}