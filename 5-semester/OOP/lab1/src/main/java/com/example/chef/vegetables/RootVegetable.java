package com.example.chef.vegetables;

public class RootVegetable extends Vegetable {
    private String color;

    public RootVegetable(String name, double caloriesPer100g, String color) {
        super(name, caloriesPer100g);
        this.color = color;
    }

    @Override
    public String getType() {
        return "ROOT";
    }

    @Override
    public String toFileString() {
        return String.format("%s;%s;%.2f;%s",
                getType(), getName(), getCaloriesPer100g(), color);
    }

    public String getColor() { return color; }

    public void setColor(String color) {
        this.color = color;
    }
}
