package com.example.chef.model;

import java.util.*;

public class Salad {
    private String name;
    private List<Ingredient> ingredients;

    public Salad(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Назва салату не може бути порожньою");
        }
        this.name = name;
        this.ingredients = new ArrayList<>();
    }

    public void addIngredient(String vegetableName, double weight) {
        ingredients.add(new Ingredient(vegetableName, weight));
    }

    public void addIngredient(Ingredient ingredient) {
        if (ingredient == null) {
            throw new IllegalArgumentException("Інгредієнт не може бути null");
        }
        ingredients.add(ingredient);
    }

    public boolean removeIngredient(int index) {
        if (index >= 0 && index < ingredients.size()) {
            ingredients.remove(index);
            return true;
        }
        return false;
    }

    public boolean removeIngredient(String vegetableName) {
        return ingredients.removeIf(ing ->
                ing.getVegetableName().equalsIgnoreCase(vegetableName));
    }

    public boolean updateWeight(String vegetableName, double newWeight) {
        for (Ingredient ing : ingredients) {
            if (ing.getVegetableName().equalsIgnoreCase(vegetableName)) {
                ing.setWeight(newWeight);
                return true;
            }
        }
        return false;
    }

    public boolean hasIngredient(String vegetableName) {
        return ingredients.stream()
                .anyMatch(ing -> ing.getVegetableName().equalsIgnoreCase(vegetableName));
    }

    public void clear() {
        ingredients.clear();
    }

    public String getName() { return name; }
    public void setName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Назва не може бути порожньою");
        }
        this.name = name;
    }

    public List<Ingredient> getIngredients() {
        return new ArrayList<>(ingredients);
    }

    public int getIngredientCount() {
        return ingredients.size();
    }

    public boolean isEmpty() {
        return ingredients.isEmpty();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("Салат: %s%n", name));
        sb.append(String.format("Інгредієнтів: %d%n", ingredients.size()));
        for (int i = 0; i < ingredients.size(); i++) {
            sb.append(String.format("  %d. %s%n", i + 1, ingredients.get(i)));
        }
        return sb.toString();
    }
}