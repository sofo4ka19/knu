package com.example.seabattle.ui;

import android.graphics.Color;
import android.graphics.Point;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.ImageButton;
import android.widget.ImageView;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.example.seabattle.R;
import com.example.seabattle.game.BattleField;
import com.example.seabattle.game.ComputerLogic;
import com.example.seabattle.game.ShotResult;
import com.example.seabattle.objects.Cell;

public class MainActivity
        extends AppCompatActivity {

    private BattleField computerField;
    private BattleField humanField;
    private ComputerLogic computer;

    private GridLayout layoutComputer;
    private GridLayout layoutHuman;

    private boolean gameRunning = false;
    private boolean turnLocked = false;

    private final int COLOR_UNKNOWN = Color.parseColor("#599ED4");
    private final int COLOR_SHIP_OWN = Color.parseColor("#455A64");
    private final int COLOR_DECK_SUNK = Color.parseColor("#B71C1C");
    private final int COLOR_MISS = Color.parseColor("#B0BEC5");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        layoutComputer = findViewById(R.id.gridComputer);
        layoutHuman = findViewById(R.id.gridHuman);
        Button btnReset = findViewById(R.id.btnNewGame);

        computer = new ComputerLogic();

        btnReset.setOnClickListener(v -> promptDifficulty());

        layoutComputer.post(this::promptDifficulty);
    }

    private void promptDifficulty() {
        initGame(false);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View dialogView = getLayoutInflater().inflate(R.layout.dialog_start_game, null);
        builder.setView(dialogView);
        builder.setCancelable(false);
        AlertDialog dialog = builder.create();

        if (dialog.getWindow() != null)
            dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);

        dialogView.findViewById(R.id.btnEasy).setOnClickListener(v -> {
            initGame(false);
            dialog.dismiss();
        });
        dialogView.findViewById(R.id.btnHard).setOnClickListener(v -> {
            initGame(true);
            dialog.dismiss();
        });
        dialog.show();
    }

    private void initGame(boolean hardMode) {
        gameRunning = true;
        turnLocked = false;

        computer.setHardMode(hardMode);
        computer.reset();

        computerField = new BattleField();
        computerField.setShipRandom();

        humanField = new BattleField();
        humanField.setShipRandom();

        renderBoards();
    }

    private void renderBoards() {
        fillGrid(layoutComputer, computerField, true);
        fillGrid(layoutHuman, humanField, false);
    }

    private void fillGrid(GridLayout gridLayout, BattleField board, boolean isEnemy) {
        gridLayout.removeAllViews();
        for (int i = 0; i < 100; i++) {
            int x = i % 10;
            int y = i / 10;

            ImageButton cellBtn = new ImageButton(this);
            GridLayout.LayoutParams params = new GridLayout.LayoutParams();
            params.width = 80;
            params.height = 80;
            params.rowSpec = GridLayout.spec(y);
            params.columnSpec = GridLayout.spec(x);
            params.setMargins(2, 2, 2, 2);
            cellBtn.setLayoutParams(params);

            Cell cell = board.getCell(x, y);

            if (!isEnemy && cell.hasShip()) {
                cellBtn.setBackgroundColor(COLOR_SHIP_OWN);
            } else {
                cellBtn.setBackgroundColor(COLOR_UNKNOWN);
            }

            cellBtn.setPadding(0,0,0,0);
            cellBtn.setScaleType(ImageView.ScaleType.CENTER_INSIDE);

            if (isEnemy) {
                cellBtn.setOnClickListener(v -> onHumanShot(x, y, cellBtn));
            } else {
                cellBtn.setEnabled(false);
            }

            gridLayout.addView(cellBtn);
        }
    }

    private void onHumanShot(int x, int y, ImageButton btn) {
        if (!gameRunning || turnLocked) return;

        ShotResult result = computerField.receiveAttack(x, y);

        if (result == ShotResult.ALREADY_HIT || result == ShotResult.INVALID) return;

        updateCellView(btn, result);

        if (result == ShotResult.SUNK) {
            updateSurroundings(computerField, layoutComputer);
        }

        if (computerField.isAllShipsDestroyed()) {
            finishGame(true);
            return;
        }

        if (result == ShotResult.MISS) {
            turnLocked = true;
            new Handler(Looper.getMainLooper()).postDelayed(this::performComputerMove, 700);
        }
    }

    private void performComputerMove() {
        if (!gameRunning) return;

        Point target = computer.getNextMove(humanField);
        ShotResult result = humanField.receiveAttack(target.x, target.y);

        // Update Human Board UI
        int index = target.y * 10 + target.x;
        ImageButton btn = (ImageButton) layoutHuman.getChildAt(index);
        updateCellView(btn, result);

        computer.processShotResult(target, result);

        if (result == ShotResult.SUNK) {
            updateSurroundings(humanField, layoutHuman);
        }

        if (humanField.isAllShipsDestroyed()) {
            finishGame(false);
            return;
        }

        if (result != ShotResult.MISS) {
            // If computer hit, it shoots again
            new Handler(Looper.getMainLooper()).postDelayed(this::performComputerMove, 800);
        } else {
            turnLocked = false; // Return control to human
        }
    }

    private void updateCellView(ImageButton btn, ShotResult result) {
        switch (result) {
            case MISS:
                btn.setBackgroundColor(COLOR_MISS);
                break;
            case HIT:
                btn.setImageResource(R.drawable.ic_explosion);
                break;
            case SUNK:
                btn.setImageResource(R.drawable.ic_explosion);
                btn.setBackgroundColor(COLOR_DECK_SUNK);
                break;
        }
        btn.setEnabled(false);
    }

    private void updateSurroundings(BattleField board, GridLayout grid) {
        for (int i = 0; i < grid.getChildCount(); i++) {
            int x = i % 10;
            int y = i / 10;
            Cell c = board.getCell(x, y);
            if (c.isHit() && !c.hasShip()) {
                grid.getChildAt(i).setBackgroundColor(COLOR_MISS);
                grid.getChildAt(i).setEnabled(false);
            }
            if (c.hasShip() && c.isHit()) {
                grid.getChildAt(i).setBackgroundColor(COLOR_DECK_SUNK);
            }
        }
    }

    private void finishGame(boolean playerWon) {
        gameRunning = false;

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View view = getLayoutInflater().inflate(R.layout.dialog_game_over, null);
        builder.setView(view);
        builder.setCancelable(false);

        AlertDialog dialog = builder.create();
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(
                    new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
        }
        android.widget.TextView tvTitle = view.findViewById(R.id.dialogTitle);
        android.widget.TextView tvMessage = view.findViewById(R.id.dialogMessage);
        Button btnMenu = view.findViewById(R.id.dialogButton);

        if (playerWon) {
            tvTitle.setText("VICTORY!");
            tvTitle.setTextColor(Color.parseColor("#4CAF50"));
            tvMessage.setText("The enemy fleet has been destroyed!");
        } else {
            tvTitle.setText("DEFEAT");
            tvTitle.setTextColor(Color.parseColor("#F44336"));
            tvMessage.setText("Your fleet has sunk");
        }

        btnMenu.setOnClickListener(v -> {
            dialog.dismiss();
            promptDifficulty();
        });

        dialog.show();
    }
}