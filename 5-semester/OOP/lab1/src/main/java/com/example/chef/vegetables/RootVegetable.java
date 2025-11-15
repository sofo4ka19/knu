package com.example.chef.vegetables;

public class RootVegetable extends Vegetable{
    private boolean requiresPeeling;
    private String color;

    /**
     * Конструктор коренеплоду.
     *
     * @param name назва
     * @param weight вага в грамах
     * @param caloriesPer100g калорійність
     * @param requiresPeeling чи потребує очищення
     * @param color колір
     */
    public RootVegetable(String name, double weight, double caloriesPer100g,
                         boolean requiresPeeling, String color) {
        super(name, weight, caloriesPer100g);
        this.requiresPeeling = requiresPeeling;
        this.color = color;
    }

    public boolean isRequiresPeeling() {
        return requiresPeeling;
    }

    public String getColor() {
        return color;
    }

    @Override
    public String getType() {
        return "Коренеплід";
    }

    @Override
    public String getDescription() {
        return String.format("%s (%s, %s)", getName(), getType(), color);
    }
}
