package com.example.seabattle.objects;

import java.util.List;

public class Ship {
    private final List<Cell> cells;

    public Ship(List<Cell> cells) {
        this.cells = cells;
        for (Cell cell : cells) {
            cell.placeShip(true);
        }
    }

    public List<Cell> getDecks() {
        return cells;
    }

    public boolean occupies(Cell cell) {
        return cells.contains(cell);
    }

    public boolean isDestroyed() {
        for (Cell deck : cells) {
            if (!deck.isHit()) {
                return false;
            }
        }
        return true;
    }
}