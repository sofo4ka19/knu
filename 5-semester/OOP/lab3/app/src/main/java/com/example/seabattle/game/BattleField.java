package com.example.seabattle.game;

import com.example.seabattle.objects.Cell;
import com.example.seabattle.objects.Ship;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class BattleField {
    private static final int SIZE = 10;
    private final Cell[][] grid = new Cell[SIZE][SIZE];
    private final List<Ship> fleet = new ArrayList<>();
    private final Random rng = new Random();

    public BattleField() {
        initGrid();
    }

    private void initGrid() {
        for (int row = 0; row < SIZE; row++) {
            for (int col = 0; col < SIZE; col++) {
                grid[col][row] = new Cell(col, row);
            }
        }
    }

    public void setShipRandom() {
        fleet.clear();
        initGrid();
        int[] shipSizes = {4, 3, 3, 2, 2, 2, 1, 1, 1, 1};

        for (int size : shipSizes) {
            boolean placed = false;
            while (!placed) {
                placed = tryPlaceShip(size);
            }
        }
    }

    private boolean tryPlaceShip(int size) {
        int x = rng.nextInt(SIZE);
        int y = rng.nextInt(SIZE);
        boolean vertical = rng.nextBoolean();

        if (isValidPlacement(x, y, size, vertical)) {
            createShip(x, y, size, vertical);
            return true;
        }
        return false;
    }

    private boolean isValidPlacement(int x, int y, int size, boolean vertical) {
        for (int i = 0; i < size; i++) {
            int cx = vertical ? x : x + i;
            int cy = vertical ? y + i : y;

            if (cx >= SIZE || cy >= SIZE) return false;

            for (int dx = -1; dx <= 1; dx++) {
                for (int dy = -1; dy <= 1; dy++) {
                    int nx = cx + dx;
                    int ny = cy + dy;
                    if (isWithinBounds(nx, ny) && grid[nx][ny].hasShip()) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

    private void createShip(int x, int y, int size, boolean vertical) {
        List<Cell> shipParts = new ArrayList<>();
        for (int i = 0; i < size; i++) {
            int cx = vertical ? x : x + i;
            int cy = vertical ? y + i : y;
            shipParts.add(grid[cx][cy]);
        }
        fleet.add(new Ship(shipParts));
    }

    public ShotResult receiveAttack(int x, int y) {
        Cell target = getCell(x, y);
        if (target == null) return ShotResult.INVALID;
        if (target.isHit()) return ShotResult.ALREADY_HIT;

        target.markHit();

        if (target.hasShip()) {
            for (Ship ship : fleet) {
                if (ship.occupies(target)) {
                    if (ship.isDestroyed()) {
                        revealSurroundings(ship);
                        return ShotResult.SUNK;
                    }
                    return ShotResult.HIT;
                }
            }
        }
        return ShotResult.MISS;
    }

    private void revealSurroundings(Ship ship) {
        for (Cell part : ship.getDecks()) {
            for (int dx = -1; dx <= 1; dx++) {
                for (int dy = -1; dy <= 1; dy++) {
                    int nx = part.getX() + dx;
                    int ny = part.getY() + dy;
                    if (isWithinBounds(nx, ny)) {
                        Cell neighbor = grid[nx][ny];
                        if (!neighbor.hasShip()) {
                            neighbor.markHit();
                        }
                    }
                }
            }
        }
    }

    public boolean isAllShipsDestroyed() {
        for (Ship s : fleet) {
            if (!s.isDestroyed()) return false;
        }
        return true;
    }

    public Cell getCell(int x, int y) {
        if (isWithinBounds(x, y)) return grid[x][y];
        return null;
    }

    public List<Ship> getFleet() { return fleet; }

    private boolean isWithinBounds(int x, int y) {
        return x >= 0 && x < SIZE && y >= 0 && y < SIZE;
    }
}