package com.exam.task2;

public class Tanker implements Ship{
    String name;
    double tankCapacity;
    String liquidType;

    public Tanker(String name, double tankCapacity, String liquidType) {
        this.name = name;
        this.tankCapacity = tankCapacity;
        this.liquidType = liquidType;
    }

    @Override
    public void displayInfo() {
        System.out.println("Танкер: " + name +
                ", місткість танків: " + tankCapacity + " м³" +
                ", рідина: " + liquidType);
    }

    @Override
    public void sail() {
        System.out.println(name + " транспортує " + liquidType);
    }
}
