package com.example.chef;

import com.example.chef.menu.ConsoleMenu;

/**
 * Головний клас програми "Шеф-кухар PRO v2.0".
 * Точка входу в додаток.
 *
 * @author Student
 * @version 2.0
 */
public class Main {

    /**
     * Головний метод програми.
     * Створює та запускає консольне меню.
     *
     * @param args аргументи командного рядка (не використовуються)
     */
    public static void main(String[] args) {
        try {
            // Створюємо та запускаємо меню
            ConsoleMenu menu = new ConsoleMenu();
            menu.run();

        } catch (Exception e) {
            // Обробка критичних помилок
            System.err.println("❌ Критична помилка програми:");
            System.err.println("   " + e.getMessage());
            e.printStackTrace();

            System.err.println("\n💡 Спробуйте:");
            System.err.println("   1. Перевірити чи існують файли data/vegetables.csv та data/salads.csv");
            System.err.println("   2. Перевірити права доступу до теки data/");
            System.err.println("   3. Перезапустити програму");

            System.exit(1);
        }
    }
}