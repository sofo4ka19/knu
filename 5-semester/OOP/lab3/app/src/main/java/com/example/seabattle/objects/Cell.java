package com.example.seabattle.objects;

public class Cell {
    private final int coordinateX; // changed from x
    private final int coordinateY; // changed from y
    private boolean containsShip;  // changed from hasShip
    private boolean isHit;  // changed from isHit

    public Cell(int x, int y) {
        this.coordinateX = x;
        this.coordinateY = y;
        this.containsShip = false;
        this.isHit = false;
    }

    public void markHit() {
        this.isHit = true;
    }

    public boolean hasShip() {
        return containsShip;
    }

    public void placeShip(boolean hasShip) {
        this.containsShip = hasShip;
    }

    public boolean isHit() {
        return isHit;
    }

    public int getX() { return coordinateX; }
    public int getY() { return coordinateY; }
}