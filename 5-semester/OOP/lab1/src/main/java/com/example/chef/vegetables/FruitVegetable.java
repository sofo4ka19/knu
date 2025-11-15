package com.example.chef.vegetables;

public class FruitVegetable extends Vegetable {
    private String color;
    private boolean hasSeed;

    public FruitVegetable(String name, double caloriesPer100g, String color, boolean hasSeed) {
        super(name, caloriesPer100g);
        this.color = color;
        this.hasSeed = hasSeed;
    }

    @Override
    public String getType() {
        return "FRUIT";
    }

    @Override
    public String toFileString() {
        return String.format("%s;%s;%.2f;%s;%s",
                getType(), getName(), getCaloriesPer100g(), color, hasSeed);
    }

    public String getColor() { return color; }
    public boolean isHasSeed() { return hasSeed; }

    public void setColor(String color) {
        this.color = color;
    }

    public void setHasSeed(boolean hasSeed) {
        this.hasSeed = hasSeed;
    }
}
