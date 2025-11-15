package com.example.chef.model;

public class Ingredient {
    private String vegetableName; // зберігаємо тільки назву!
    private double weight;

    public Ingredient(String vegetableName, double weight) {
        if (vegetableName == null || vegetableName.trim().isEmpty()) {
            throw new IllegalArgumentException("Назва овочу не може бути порожньою");
        }
        if (weight <= 0) {
            throw new IllegalArgumentException("Вага повинна бути більше 0");
        }
        this.vegetableName = vegetableName;
        this.weight = weight;
    }

    public String getVegetableName() { return vegetableName; }
    public double getWeight() { return weight; }

    public void setWeight(double weight) {
        if (weight <= 0) {
            throw new IllegalArgumentException("Вага повинна бути більше 0");
        }
        this.weight = weight;
    }

    public String toFileString() {
        return String.format("%s;%.2f", vegetableName, weight);
    }

    @Override
    public String toString() {
        return String.format("%s: %.1f г", vegetableName, weight);
    }
}
