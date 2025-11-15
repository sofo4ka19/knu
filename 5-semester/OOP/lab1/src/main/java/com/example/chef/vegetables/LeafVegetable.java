package com.example.chef.vegetables;

public class LeafVegetable extends Vegetable{
    private String leafType;
    private boolean isCrispy;

    /**
     * Конструктор листового овочу.
     *
     * @param name назва
     * @param weight вага в грамах
     * @param caloriesPer100g калорійність
     * @param leafType тип листя
     * @param isCrispy чи хрусткий
     */
    public LeafVegetable(String name, double weight, double caloriesPer100g,
                         String leafType, boolean isCrispy) {
        super(name, weight, caloriesPer100g);
        this.leafType = leafType;
        this.isCrispy = isCrispy;
    }

    public String getLeafType() {
        return leafType;
    }

    public boolean isCrispy() {
        return isCrispy;
    }

    @Override
    public String getType() {
        return "Листовий";
    }

    @Override
    public String getDescription() {
        return String.format("%s (%s, %s)", getName(), getType(), leafType);
    }
}
