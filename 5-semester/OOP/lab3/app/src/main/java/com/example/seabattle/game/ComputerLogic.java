package com.example.seabattle.game;

import android.graphics.Point;
import com.example.seabattle.objects.Cell;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.Stack;

public class ComputerLogic {
    private final Stack<Point> priorityTargets = new Stack<>();
    private final Random random = new Random();
    private Point firstHitLocation = null;
    private Point lastHitLocation = null;
    private boolean hardMode = false;

    public void setHardMode(boolean isHard) {
        this.hardMode = isHard;
    }

    public void reset() {
        priorityTargets.clear();
        firstHitLocation = null;
        lastHitLocation = null;
    }

    // Головний метод, який Activity буде викликати
    public Point getNextMove(BattleField opponentBoard) {
        if (hardMode && !priorityTargets.isEmpty()) {
            return priorityTargets.pop();
        }

        // Random shot logic
        int x, y;
        do {
            x = random.nextInt(10);
            y = random.nextInt(10);
        } while (opponentBoard.getCell(x, y).isHit());

        return new Point(x, y);
    }

    public void processShotResult(Point point, ShotResult result) {
        if (!hardMode) return;

        if (result == ShotResult.SUNK) {
            priorityTargets.clear();
            firstHitLocation = null;
            lastHitLocation = null;
        } else if (result == ShotResult.HIT) {
            handleHit(point.x, point.y);
        }
    }

    private void handleHit(int x, int y) {
        if (firstHitLocation == null) {
            firstHitLocation = new Point(x, y);
            lastHitLocation = new Point(x, y);
            addSurroundingCells(x, y);
        } else {
            boolean vertical = (x == firstHitLocation.x);
            boolean horizontal = (y == firstHitLocation.y);

            filterTargets(vertical, horizontal);

            // Calculate next logical step based on direction
            int dx = x - lastHitLocation.x;
            int dy = y - lastHitLocation.y;

            // Try to continue in that direction
            pushIfValid(x + dx, y + dy);

            if (priorityTargets.size() < 2) {
                int revDx = (dx != 0) ? -dx : 0;
                int revDy = (dy != 0) ? -dy : 0;
                pushIfValid(firstHitLocation.x + revDx, firstHitLocation.y + revDy);
            }

            lastHitLocation = new Point(x, y);
        }
    }

    private void addSurroundingCells(int x, int y) {
        List<Point> potential = new ArrayList<>();
        potential.add(new Point(x + 1, y));
        potential.add(new Point(x - 1, y));
        potential.add(new Point(x, y + 1));
        potential.add(new Point(x, y - 1));
        Collections.shuffle(potential);

        for(Point p : potential) {
            if (isValidCoordinate(p.x, p.y)) priorityTargets.push(p);
        }
    }

    private void filterTargets(boolean keepVertical, boolean keepHorizontal) {
        if (!keepVertical && !keepHorizontal) return;

        Stack<Point> filtered = new Stack<>();
        for (Point p : priorityTargets) {
            if (keepVertical && p.x == firstHitLocation.x) filtered.push(p);
            else if (keepHorizontal && p.y == firstHitLocation.y) filtered.push(p);
        }
        priorityTargets.clear();
        priorityTargets.addAll(filtered);
    }

    private void pushIfValid(int x, int y) {
        if (isValidCoordinate(x, y)) {
            priorityTargets.push(new Point(x, y));
        }
    }

    private boolean isValidCoordinate(int x, int y) {
        return x >= 0 && x < 10 && y >= 0 && y < 10;
    }
}