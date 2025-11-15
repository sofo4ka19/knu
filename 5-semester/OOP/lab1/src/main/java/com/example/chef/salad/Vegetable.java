package com.example.chef.salad;

import java.util.Objects;

/**
 * Абстрактний базовий клас для всіх овочів.
 * Демонструє принципи інкапсуляції та абстракції.
 */
public abstract class Vegetable {
    private String name;
    private double weight; // у грамах
    private double caloriesPer100g; // калорійність на 100г

    /**
     * Конструктор для створення овочу.
     *
     * @param name назва овочу
     * @param weight вага в грамах
     * @param caloriesPer100g калорійність на 100г
     * @throws IllegalArgumentException якщо параметри некоректні
     */
    public Vegetable(String name, double weight, double caloriesPer100g) {
        validateName(name);
        validateWeight(weight);
        validateCalories(caloriesPer100g);

        this.name = name;
        this.weight = weight;
        this.caloriesPer100g = caloriesPer100g;
    }

    private void validateName(String name) {
        if (name == null || name.trim().isEmpty()) {
            throw new IllegalArgumentException("Назва овочу не може бути порожньою");
        }
        //перевірка на число
    }

    private void validateWeight(double weight) {
        if (weight <= 0) {
            throw new IllegalArgumentException("Вага повинна бути більше 0");
        }
    }

    private void validateCalories(double calories) {
        if (calories < 0) {
            throw new IllegalArgumentException("Калорійність не може бути від'ємною");
        }
    }

    /**
     * Обчислює загальну калорійність овочу на основі його ваги.
     *
     * @return загальна калорійність
     */
    public double getTotalCalories() {
        return (weight / 100.0) * caloriesPer100g;
    }

    /**
     * Повертає тип овочу (визначається в підкласах).
     * Демонструє поліморфізм.
     *
     * @return тип овочу
     */
    public abstract String getType();

    /**
     * Повертає детальний опис овочу.
     * Може бути перевизначений у підкласах.
     *
     * @return опис овочу
     */
    public String getDescription() {
        return String.format("%s (%s)", name, getType());
    }

    // Геттери (інкапсуляція)
    public String getName() {
        return name;
    }

    public double getWeight() {
        return weight;
    }

    public double getCaloriesPer100g() {
        return caloriesPer100g;
    }

    // Сеттери з валідацією
    public void setWeight(double weight) {
        validateWeight(weight);
        this.weight = weight;
    }

    public void setCaloriesPer100g(double caloriesPer100g) {
        validateCalories(caloriesPer100g);
        this.caloriesPer100g = caloriesPer100g;
    }

}