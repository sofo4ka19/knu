package com.exam;
import com.exam.task1.ObjectList;
import com.exam.task2.*;

import java.io.*;
import java.util.*;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) {
        // ЗАВДАННЯ 1
        System.out.println("=== ЗАВДАННЯ 1 ===\n");
        try {
            // Створення тестового файлу
            PrintWriter pw = new PrintWriter("objects.txt");
            pw.println("Компютер");
            pw.println("Принтер");
            pw.println("Монітор");
            pw.println("Компютер");
            pw.println("Принтер");
            pw.close();

            ObjectList.execute();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // ЗАВДАННЯ 2
        // ЗАВДАННЯ 2
        System.out.println("\n\n=== ЗАВДАННЯ 2 ===\n");

        // Поліморфізм - змінна типу Ship може зберігати будь-який корабель
        Ship cargo = new CargoShip("Атлантік", 35000);
        Ship tanker = new Tanker("Нептун", 60000, "Нафта");

        cargo.displayInfo();
        cargo.sail();

        System.out.println();

        tanker.displayInfo();
        tanker.sail();

        // Демонстрація поліморфізму зі списком
        System.out.println("\nФлот:");
        List<Ship> fleet = Arrays.asList(cargo, tanker);
        for (Ship ship : fleet) {
            ship.sail();
        }
    }
}