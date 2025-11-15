package com.example.chef.vegetables;

public class LeafVegetable extends Vegetable {
    private String leafType;
    private boolean isCrispy;

    public LeafVegetable(String name, double caloriesPer100g, String leafType, boolean isCrispy) {
        super(name, caloriesPer100g);
        this.leafType = leafType;
        this.isCrispy = isCrispy;
    }

    @Override
    public String getType() {
        return "LEAF";
    }

    @Override
    public String toFileString() {
        return String.format("%s;%s;%.2f;%s;%s",
                getType(), getName(), getCaloriesPer100g(), leafType, isCrispy);
    }

    public String getLeafType() { return leafType; }
    public boolean isCrispy() { return isCrispy; }

    public void setLeafType(String leafType) {
        this.leafType = leafType;
    }

    public void setCrispy(boolean crispy) {
        isCrispy = crispy;
    }
}
