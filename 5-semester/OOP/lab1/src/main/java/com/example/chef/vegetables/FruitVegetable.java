package com.example.chef.vegetables;

public class FruitVegetable extends Vegetable {
    private String color;
    private boolean hasSeed;

    /**
     * Конструктор плодового овочу.
     *
     * @param name назва
     * @param weight вага в грамах
     * @param caloriesPer100g калорійність
     * @param color колір
     * @param hasSeed чи має насіння
     */
    public FruitVegetable(String name, double weight, double caloriesPer100g,
                          String color, boolean hasSeed) {
        super(name, weight, caloriesPer100g);
        this.color = color;
        this.hasSeed = hasSeed;
    }

    public String getColor() {
        return color;
    }

    public boolean isHasSeed() {
        return hasSeed;
    }

    @Override
    public String getType() {
        return "Плодовий";
    }

    @Override
    public String getDescription() {
        return String.format("%s (%s, %s)", getName(), getType(), color);
    }
}
