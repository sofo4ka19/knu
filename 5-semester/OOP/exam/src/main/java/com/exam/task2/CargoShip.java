package com.exam.task2;

public class CargoShip implements Ship {
    String name;
    double cargoCapacity;

    public CargoShip(String name, double cargoCapacity) {
        this.name = name;
        this.cargoCapacity = cargoCapacity;
    }

    @Override
    public void displayInfo() {
        System.out.println("Вантажний корабель: " + name +
                ", вантажомісткість: " + cargoCapacity + " т");
    }

    @Override
    public void sail() {
        System.out.println(name + " перевозить вантаж");
    }
}
