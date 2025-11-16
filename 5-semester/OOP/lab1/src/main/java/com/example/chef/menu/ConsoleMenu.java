package com.example.chef.menu;

import com.example.chef.model.*;
import com.example.chef.service.*;
import java.util.*;

public class ConsoleMenu {
    private final Scanner scanner;
    private final VegetableService vegetableService;
    private final SaladService saladService;
    private Salad currentSalad;

    public ConsoleMenu() {
        this.scanner = new Scanner(System.in);
        this.vegetableService = new VegetableService();
        this.saladService = new SaladService(vegetableService);

        // Встановлюємо двосторонній зв'язок для перевірки використання
        this.vegetableService.setSaladService(saladService);
    }

    public void run() {
        printWelcome();
        loadData();

        boolean running = true;
        while (running) {
            printMainMenu();
            int choice = readIntInput("Ваш вибір: ");

            switch (choice) {
                case 1: manageVegetables(); break;
                case 2: manageSalads(); break;
                case 3: manageIngredients(); break;
                case 4: viewSaladInfo(); break;
                case 5: sortAndSearch(); break;
                case 6: saveData(); break;
                case 0:
                    saveBeforeExit();
                    running = false;
                    break;
                default:
                    System.out.println("❌ Невірний вибір!");
            }
        }

        scanner.close();
    }

    // ============================================
    // ГОЛОВНЕ МЕНЮ
    // ============================================

    private void printMainMenu() {
        clearScreen();
        System.out.println("\n╔════════════════════════════════════╗");
        System.out.println("║       🥗 ГОЛОВНЕ МЕНЮ 🥗          ║");
        System.out.println("╠════════════════════════════════════╣");

        if (currentSalad != null) {
            System.out.printf("║ 🎯 Активний: %-21s ║%n",
                    truncate(currentSalad.getName(), 21));
        }

        System.out.println("╠════════════════════════════════════╣");
        System.out.println("║ 1. 🥬 Реєстр овочів               ║");
        System.out.println("║ 2. 🥗 Управління салатами         ║");
        System.out.println("║ 3. 🍅 Управління інгредієнтами    ║");
        System.out.println("║ 4. 📊 Інформація про салат        ║");
        System.out.println("║ 5. 🔍 Сортування та пошук         ║");
        System.out.println("║ 6. 💾 Зберегти все                ║");
        System.out.println("║ 0. 🚪 Вихід                       ║");
        System.out.println("╚════════════════════════════════════╝");
    }

    // ============================================
    // 1. РЕЄСТР ОВОЧІВ
    // ============================================

    private void manageVegetables() {
        while (true) {
            clearScreen();
            System.out.println("\n┌─────────────────────────────────┐");
            System.out.println("│      🥬 РЕЄСТР ОВОЧІВ          │");
            System.out.printf("│      Всього: %-18d │%n", vegetableService.getCount());
            System.out.println("├─────────────────────────────────┤");
            System.out.println("│ 1. Показати всі овочі           │");
            System.out.println("│ 2. Додати новий овоч            │");
            System.out.println("│ 3. Редагувати овоч              │");
            System.out.println("│ 4. Видалити овоч                │");
            System.out.println("│ 5. Пошук овочів                 │");
            System.out.println("│ 6. Статистика використання      │");
            System.out.println("│ 0. Назад                        │");
            System.out.println("└─────────────────────────────────┘");

            int choice = readIntInput("Вибір: ");

            switch (choice) {
                case 1: showAllVegetables(); break;
                case 2: addVegetable(); break;
                case 3: editVegetable(); break;
                case 4: deleteVegetable(); break;
                case 5: searchVegetables(); break;
                case 6: showVegetableStatistics(); break;
                case 0: return;
                default: System.out.println("❌ Невірний вибір!");
            }

        }
    }

    private void showAllVegetables() {
        Collection<Vegetable> vegetables = vegetableService.getAllVegetables();

        if (vegetables.isEmpty()) {
            System.out.println("\n⚠️  Реєстр овочів порожній.");
            return;
        }

        System.out.println("\n📋 РЕЄСТР ОВОЧІВ:");
        System.out.println("═══════════════════════════════════════════════════════════════");
        System.out.printf("%-3s %-20s %-10s %-10s %-15s%n", "#", "Назва", "Тип", "Калорії", "Використання");
        System.out.println("───────────────────────────────────────────────────────────────");

        int index = 1;
        for (Vegetable veg : vegetables) {
            List<String> usedIn = vegetableService.getUsageInfo(veg.getName());
            String usage = usedIn.isEmpty() ? "—" : usedIn.size() + " салатів";

            System.out.printf("%-3d %-20s %-10s %-10.1f %-15s%n",
                    index++,
                    truncate(veg.getName(), 20),
                    veg.getType(),
                    veg.getCaloriesPer100g(),
                    usage);
        }
        System.out.println("═══════════════════════════════════════════════════════════════");
    }

    private void addVegetable() {
        System.out.println("\n🆕 ДОДАВАННЯ ОВОЧУ");
        System.out.println("───────────────────────────────────");

        System.out.print("Назва: ");
        String name = scanner.nextLine().trim();

        if (vegetableService.exists(name)) {
            System.out.println("❌ Овоч з такою назвою вже існує!");
            return;
        }

        System.out.println("\nОберіть тип:");
        System.out.println("1. ROOT  - Коренеплід");
        System.out.println("2. LEAF  - Листовий");
        System.out.println("3. FRUIT - Плодовий");
        int type = readIntInput("Тип: ");

        double calories = readDoubleInput("Калорійність (ккал/100г): ");

        Vegetable vegetable = null;

        try {
            switch (type) {
                case 1: // ROOT
                    System.out.print("Колір: ");
                    String color1 = scanner.nextLine().trim();
                    System.out.print("Потребує очищення (true/false): ");
                    boolean peeling = readBooleanInput();
                    vegetable = new RootVegetable(name, calories, color1);
                    break;

                case 2: // LEAF
                    System.out.print("Тип листя: ");
                    String leafType = scanner.nextLine().trim();
                    System.out.print("Хрусткий (true/false): ");
                    boolean crispy = readBooleanInput();
                    vegetable = new LeafVegetable(name, calories, leafType, crispy);
                    break;

                case 3: // FRUIT
                    System.out.print("Колір: ");
                    String color2 = scanner.nextLine().trim();
                    System.out.print("Має насіння (true/false): ");
                    boolean seed = readBooleanInput();
                    vegetable = new FruitVegetable(name, calories, color2, seed);
                    break;

                default:
                    System.out.println("❌ Невірний тип!");
                    return;
            }

            if (vegetableService.addVegetable(vegetable)) {
                System.out.println("✅ Овоч успішно додано!");
            } else {
                System.out.println("❌ Помилка додавання овочу!");
            }

        } catch (IllegalArgumentException e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    private void editVegetable() {
        System.out.print("\n✏️  Введіть назву овочу для редагування: ");
        String oldName = scanner.nextLine().trim();

        Vegetable oldVeg = vegetableService.getVegetable(oldName);
        if (oldVeg == null) {
            System.out.println("❌ Овоч не знайдено!");
            return;
        }

        System.out.println("\nПоточні дані:");
        System.out.println(oldVeg);

        // Показуємо де використовується
        List<String> usedIn = vegetableService.getUsageInfo(oldName);
        if (!usedIn.isEmpty()) {
            System.out.println("\n⚠️  Цей овоч використовується в салатах:");
            usedIn.forEach(s -> System.out.println("   - " + s));
        }

        System.out.println("\n💡 Натисніть Enter щоб залишити значення без змін");

        System.out.print("Нова назва [" + oldVeg.getName() + "]: ");
        String newName = scanner.nextLine().trim();
        if (newName.isEmpty()) newName = oldVeg.getName();

        // Якщо змінюється назва - попереджаємо
        if (!newName.equalsIgnoreCase(oldName) && !usedIn.isEmpty()) {
            System.out.println("\n⚠️  УВАГА! Зміна назви оновить всі салати де використовується цей овоч!");
            System.out.print("Продовжити? (так/ні): ");
            String confirm = scanner.nextLine().trim().toLowerCase();
            if (!confirm.equals("так") && !confirm.equals("yes")) {
                System.out.println("❌ Скасовано.");
                return;
            }
        }

        System.out.print("Нова калорійність [" + oldVeg.getCaloriesPer100g() + "]: ");
        String calStr = scanner.nextLine().trim();
        double newCalories = calStr.isEmpty() ?
                oldVeg.getCaloriesPer100g() : Double.parseDouble(calStr);

        Vegetable newVeg = null;

        try {
            if (oldVeg instanceof RootVegetable) {
                RootVegetable rv = (RootVegetable) oldVeg;
                System.out.print("Колір [" + rv.getColor() + "]: ");
                String color = scanner.nextLine().trim();
                if (color.isEmpty()) color = rv.getColor();

                newVeg = new RootVegetable(newName, newCalories, color);

            } else if (oldVeg instanceof LeafVegetable) {
                LeafVegetable lv = (LeafVegetable) oldVeg;
                System.out.print("Тип листя [" + lv.getLeafType() + "]: ");
                String leafType = scanner.nextLine().trim();
                if (leafType.isEmpty()) leafType = lv.getLeafType();

                System.out.print("Хрусткий [" + lv.isCrispy() + "]: ");
                String crispyStr = scanner.nextLine().trim();
                boolean crispy = crispyStr.isEmpty() ?
                        lv.isCrispy() : Boolean.parseBoolean(crispyStr);

                newVeg = new LeafVegetable(newName, newCalories, leafType, crispy);

            } else if (oldVeg instanceof FruitVegetable) {
                FruitVegetable fv = (FruitVegetable) oldVeg;
                System.out.print("Колір [" + fv.getColor() + "]: ");
                String color = scanner.nextLine().trim();
                if (color.isEmpty()) color = fv.getColor();

                System.out.print("Має насіння [" + fv.isHasSeed() + "]: ");
                String seedStr = scanner.nextLine().trim();
                boolean seed = seedStr.isEmpty() ?
                        fv.isHasSeed() : Boolean.parseBoolean(seedStr);

                newVeg = new FruitVegetable(newName, newCalories, color, seed);
            }

            if (vegetableService.updateVegetable(oldName, newVeg)) {
                System.out.println("✅ Овоч успішно оновлено!");
                if (!newName.equalsIgnoreCase(oldName)) {
                    System.out.println("✅ Оновлено в " + usedIn.size() + " салатах");
                }
            } else {
                System.out.println("❌ Помилка оновлення!");
            }

        } catch (Exception e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    private void deleteVegetable() {
        System.out.print("\n🗑️  Введіть назву овочу для видалення: ");
        String name = scanner.nextLine().trim();

        if (!vegetableService.exists(name)) {
            System.out.println("❌ Овоч не знайдено!");
            return;
        }

        // Перевіряємо використання
        List<String> usedIn = vegetableService.getUsageInfo(name);

        if (!usedIn.isEmpty()) {
            System.out.println("\n⚠️  УВАГА! Цей овоч використовується в салатах:");
            usedIn.forEach(s -> System.out.println("   - " + s));
            System.out.println("\n❌ Неможливо видалити овоч поки він використовується!");
            System.out.println("💡 Спочатку видаліть його з салатів або видаліть ці салати.");
            return;
        }

        System.out.print("⚠️  Ви впевнені? (так/ні): ");
        String confirm = scanner.nextLine().trim().toLowerCase();

        if (confirm.equals("так") || confirm.equals("yes") || confirm.equals("y")) {
            try {
                if (vegetableService.deleteVegetable(name)) {
                    System.out.println("✅ Овоч видалено!");
                } else {
                    System.out.println("❌ Помилка видалення!");
                }
            } catch (IllegalStateException e) {
                System.out.println("❌ " + e.getMessage());
            }
        } else {
            System.out.println("❌ Скасовано.");
        }
    }

    private void searchVegetables() {
        System.out.println("\n🔍 ПОШУК ОВОЧІВ");
        System.out.println("1. За типом");
        System.out.println("2. За діапазоном калорійності");
        System.out.println("3. За назвою (частковий збіг)");
        int choice = readIntInput("Вибір: ");

        switch (choice) {
            case 1:
                System.out.println("\nТипи: ROOT, LEAF, FRUIT");
                System.out.print("Введіть тип: ");
                String type = scanner.nextLine().trim();
                List<Vegetable> byType = vegetableService.findByType(type);
                displayVegetableList(byType);
                break;

            case 2:
                double min = readDoubleInput("Мінімальна калорійність: ");
                double max = readDoubleInput("Максимальна калорійність: ");
                List<Vegetable> byCalories = vegetableService.findByCalorieRange(min, max);
                displayVegetableList(byCalories);
                break;

            case 3:
                System.out.print("Введіть частину назви: ");
                String searchTerm = scanner.nextLine().trim().toLowerCase();
                List<Vegetable> byName = vegetableService.getAllVegetables().stream()
                        .filter(v -> v.getName().toLowerCase().contains(searchTerm))
                        .toList();
                displayVegetableList(byName);
                break;
        }
    }

    private void showVegetableStatistics() {
        System.out.println("\n📊 СТАТИСТИКА ВИКОРИСТАННЯ ОВОЧІВ");
        System.out.println("═══════════════════════════════════════════════════");

        Map<String, Integer> stats = saladService.getVegetableUsageStatistics();

        if (stats.isEmpty()) {
            System.out.println("⚠️  Немає даних для відображення.");
            return;
        }

        List<Map.Entry<String, Integer>> sorted = saladService.getMostUsedVegetables(100);

        System.out.printf("%-30s %-15s%n", "Овоч", "Салатів");
        System.out.println("───────────────────────────────────────────────────");

        for (Map.Entry<String, Integer> entry : sorted) {
            System.out.printf("%-30s %-15d%n",
                    truncate(entry.getKey(), 30),
                    entry.getValue());
        }

        System.out.println("═══════════════════════════════════════════════════");
        System.out.printf("Всього унікальних овочів використано: %d%n", stats.size());
    }

    private void displayVegetableList(List<Vegetable> vegetables) {
        if (vegetables.isEmpty()) {
            System.out.println("\n⚠️  Нічого не знайдено.");
            return;
        }

        System.out.println("\n📋 РЕЗУЛЬТАТИ ПОШУКУ:");
        System.out.println("───────────────────────────────────────────────────");
        for (int i = 0; i < vegetables.size(); i++) {
            System.out.printf("%d. %s%n", i + 1, vegetables.get(i));
        }
        System.out.println("───────────────────────────────────────────────────");
        System.out.printf("Знайдено: %d%n", vegetables.size());
    }

    // ============================================
    // 2. УПРАВЛІННЯ САЛАТАМИ
    // ============================================

    private void manageSalads() {
        while (true) {
            clearScreen();
            System.out.println("\n┌─────────────────────────────────┐");
            System.out.println("│   🥗 УПРАВЛІННЯ САЛАТАМИ       │");
            System.out.printf("│   Всього: %-21d │%n", saladService.getCount());
            System.out.println("├─────────────────────────────────┤");
            System.out.println("│ 1. Показати всі салати          │");
            System.out.println("│ 2. Створити новий салат         │");
            System.out.println("│ 3. Вибрати активний салат       │");
            System.out.println("│ 4. Перейменувати салат          │");
            System.out.println("│ 5. Видалити салат               │");
            System.out.println("│ 6. Клонувати салат              │");
            System.out.println("│ 0. Назад                        │");
            System.out.println("└─────────────────────────────────┘");

            int choice = readIntInput("Вибір: ");

            switch (choice) {
                case 1: showAllSalads(); break;
                case 2: createSalad(); break;
                case 3: selectSalad(); break;
                case 4: renameSalad(); break;
                case 5: deleteSalad(); break;
                case 6: cloneSalad(); break;
                case 0: return;
                default: System.out.println("❌ Невірний вибір!");
            }

        }
    }

    private void showAllSalads() {
        Collection<Salad> salads = saladService.getAllSalads();

        if (salads.isEmpty()) {
            System.out.println("\n⚠️  Салати відсутні.");
            return;
        }

        System.out.println("\n📋 СПИСОК САЛАТІВ:");
        System.out.println("═══════════════════════════════════════════════════════════════");
        System.out.printf("%-3s %-25s %-12s %-12s %-12s%n", "#", "Назва", "Інгредієнтів", "Вага (г)", "Калорії");
        System.out.println("───────────────────────────────────────────────────────────────");

        int index = 1;
        for (Salad salad : salads) {
            String active = (salad == currentSalad) ? " ⭐" : "";
            double weight = saladService.calculateWeight(salad.getName());
            double calories = saladService.calculateCalories(salad.getName());

            System.out.printf("%-3d %-25s %-12d %-12.1f %-12.1f%s%n",
                    index++,
                    truncate(salad.getName(), 25),
                    salad.getIngredientCount(),
                    weight,
                    calories,
                    active);
        }
        System.out.println("═══════════════════════════════════════════════════════════════");
    }

    private void createSalad() {
        System.out.print("\n📝 Введіть назву нового салату: ");
        String name = scanner.nextLine().trim();

        if (name.isEmpty()) {
            System.out.println("❌ Назва не може бути порожньою!");
            return;
        }

        if (saladService.exists(name)) {
            System.out.println("❌ Салат з такою назвою вже існує!");
            return;
        }

        try {
            Salad salad = new Salad(name);
            if (saladService.createSalad(salad)) {
                currentSalad = salad;
                System.out.println("✅ Салат '" + name + "' створено і активовано!");
                do {
                    addIngredient();
                    System.out.print("\n📝 Введіть 0 якщо не бажаєте далі додавати інгредієнти: ");
                    String exit = scanner.nextLine().trim();
                    if (exit.equals("0")) {
                        break;
                    }
                } while (true);
            } else {
                System.out.println("❌ Помилка створення салату!");
            }
        } catch (Exception e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    private void selectSalad() {
        showAllSalads();

        if (saladService.getCount() == 0) {
            return;
        }

        System.out.print("\n🎯 Введіть назву салату: ");
        String name = scanner.nextLine().trim();

        Salad salad = saladService.getSalad(name);
        if (salad != null) {
            currentSalad = salad;
            System.out.println("✅ Активовано: " + name);
        } else {
            System.out.println("❌ Салат не знайдено!");
        }
    }

    private void renameSalad() {
        showAllSalads();

        System.out.print("\n✏️  Стара назва: ");
        String oldName = scanner.nextLine().trim();

        if (!saladService.exists(oldName)) {
            System.out.println("❌ Салат не знайдено!");
            return;
        }

        System.out.print("Нова назва: ");
        String newName = scanner.nextLine().trim();

        if (newName.isEmpty()) {
            System.out.println("❌ Назва не може бути порожньою!");
            return;
        }

        try {
            if (saladService.renameSalad(oldName, newName)) {
                if (currentSalad != null && currentSalad.getName().equalsIgnoreCase(oldName)) {
                    currentSalad = saladService.getSalad(newName);
                }
                System.out.println("✅ Салат перейменовано!");
            } else {
                System.out.println("❌ Не вдалося перейменувати!");
            }
        } catch (Exception e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    private void deleteSalad() {
        showAllSalads();

        System.out.print("\n🗑️  Назва салату для видалення: ");
        String name = scanner.nextLine().trim();

        if (!saladService.exists(name)) {
            System.out.println("❌ Салат не знайдено!");
            return;
        }

        System.out.print("⚠️  Ви впевнені? (так/ні): ");
        String confirm = scanner.nextLine().trim().toLowerCase();

        if (confirm.equals("так") || confirm.equals("yes") || confirm.equals("y")) {
            if (saladService.deleteSalad(name)) {
                if (currentSalad != null && currentSalad.getName().equalsIgnoreCase(name)) {
                    currentSalad = null;
                }
                System.out.println("✅ Салат видалено!");
            } else {
                System.out.println("❌ Помилка видалення!");
            }
        } else {
            System.out.println("❌ Скасовано.");
        }
    }

    private void cloneSalad() {
        showAllSalads();

        System.out.print("\n📋 Назва салату для клонування: ");
        String sourceName = scanner.nextLine().trim();

        Salad source = saladService.getSalad(sourceName);
        if (source == null) {
            System.out.println("❌ Салат не знайдено!");
            return;
        }

        System.out.print("Назва нової копії: ");
        String newName = scanner.nextLine().trim();

        if (saladService.exists(newName)) {
            System.out.println("❌ Салат з такою назвою вже існує!");
            return;
        }

        try {
            Salad clone = new Salad(newName);
            for (Ingredient ing : source.getIngredients()) {
                clone.addIngredient(ing.getVegetableName(), ing.getWeight());
            }

            if (saladService.createSalad(clone)) {
                System.out.println("✅ Салат клоновано!");
            }
        } catch (Exception e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    // ============================================
    // 3. УПРАВЛІННЯ ІНГРЕДІЄНТАМИ
    // ============================================

    private void manageIngredients() {
        if (!checkActiveSalad()) return;

        while (true) {
            clearScreen();
            System.out.println("\n┌─────────────────────────────────┐");
            System.out.println("│   🍅 УПРАВЛІННЯ ІНГРЕДІЄНТАМИ   │");
            System.out.printf("│   Салат: %-22s │%n", truncate(currentSalad.getName(), 22));
            System.out.println("├─────────────────────────────────┤");
            System.out.println("│ 1. Показати інгредієнти         │");
            System.out.println("│ 2. Додати інгредієнт            │");
            System.out.println("│ 3. Видалити інгредієнт          │");
            System.out.println("│ 4. Змінити вагу інгредієнта     │");
            System.out.println("│ 5. Очистити салат               │");
            System.out.println("│ 0. Назад                        │");
            System.out.println("└─────────────────────────────────┘");

            int choice = readIntInput("Вибір: ");

            switch (choice) {
                case 1: showIngredients(); break;
                case 2: addIngredient(); break;
                case 3: removeIngredient(); break;
                case 4: updateIngredientWeight(); break;
                case 5: clearSalad(); break;
                case 0: return;
                default: System.out.println("❌ Невірний вибір!");
            }
        }
    }

    private void showIngredients() {
        System.out.println("\n" + saladService.getSaladDetails(currentSalad.getName()));
    }
    private void addIngredient() {
        // Показуємо доступні овочі
        Collection<Vegetable> vegetables = vegetableService.getAllVegetables();

        if (vegetables.isEmpty()) {
            System.out.println("\n⚠️  Реєстр овочів порожній!");
            return;
        }

        System.out.println("\n📋 ДОСТУПНІ ОВОЧІ:");
        System.out.println("───────────────────────────────────────────────────");
        int index = 1;
        List<Vegetable> vegList = new ArrayList<>(vegetables);
        for (Vegetable veg : vegList) {
            System.out.printf("%d. %s (%.1f ккал/100г)%n",
                    index++, veg.getName(), veg.getCaloriesPer100g());
        }
        System.out.println("───────────────────────────────────────────────────");

        System.out.print("\nВиберіть овоч (номер або назва): ");
        String input = scanner.nextLine().trim();

        Vegetable vegetable = null;

        try {
            int num = Integer.parseInt(input);
            if (num > 0 && num <= vegList.size()) {
                vegetable = vegList.get(num - 1);
            }
        } catch (NumberFormatException e) {
            vegetable = vegetableService.getVegetable(input);
        }

        if (vegetable == null) {
            System.out.println("❌ Овоч не знайдено!");
            return;
        }

        double weight = readDoubleInput("Вага (г): ");

        try {
            if (saladService.addIngredient(currentSalad.getName(), vegetable.getName(), weight)) {
                System.out.println("✅ Інгредієнт додано!");
            } else {
                System.out.println("❌ Помилка додавання!");
            }
        } catch (Exception e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    private void removeIngredient() {
        if (currentSalad.isEmpty()) {
            System.out.println("\n⚠️  Салат порожній!");
            return;
        }

        showIngredients();

        System.out.print("\n🗑️  Номер інгредієнта для видалення (або 0 для скасування): ");
        int index = readIntInput("") - 1;

        if (index == -1) {
            System.out.println("❌ Скасовано.");
            return;
        }

        if (currentSalad.removeIngredient(index)) {
            System.out.println("✅ Інгредієнт видалено!");
        } else {
            System.out.println("❌ Некоректний номер!");
        }
    }

    private void updateIngredientWeight() {
        if (currentSalad.isEmpty()) {
            System.out.println("\n⚠️  Салат порожній!");
            return;
        }

        showIngredients();

        System.out.print("\n✏️  Номер інгредієнта: ");
        int index = readIntInput("") - 1;

        if (index < 0 || index >= currentSalad.getIngredientCount()) {
            System.out.println("❌ Некоректний номер!");
            return;
        }

        double newWeight = readDoubleInput("Нова вага (г): ");

        if (currentSalad.updateWeight(
                currentSalad.getIngredients().get(index).getVegetableName(),
                newWeight)) {
            System.out.println("✅ Вага оновлена!");
        } else {
            System.out.println("❌ Помилка оновлення!");
        }
    }

    private void clearSalad() {
        if (currentSalad.isEmpty()) {
            System.out.println("\n⚠️  Салат вже порожній!");
            return;
        }

        System.out.print("⚠️  Очистити салат? (так/ні): ");
        String confirm = scanner.nextLine().trim().toLowerCase();

        if (confirm.equals("так") || confirm.equals("yes") || confirm.equals("y")) {
            currentSalad.clear();
            System.out.println("✅ Салат очищено!");
        } else {
            System.out.println("❌ Скасовано.");
        }
    }

    // ============================================
    // 4. ІНФОРМАЦІЯ ПРО САЛАТ
    // ============================================

    private void viewSaladInfo() {
        if (!checkActiveSalad()) return;

        while (true) {
            clearScreen();
            System.out.println("\n┌─────────────────────────────────┐");
            System.out.println("│   📊 ІНФОРМАЦІЯ ПРО САЛАТ      │");
            System.out.println("├─────────────────────────────────┤");
            System.out.println("│ 1. Детальна інформація          │");
            System.out.println("│ 2. Калорійність                 │");
            System.out.println("│ 3. Список інгредієнтів          │");
            System.out.println("│ 4. Статистика                   │");
            System.out.println("│ 0. Назад                        │");
            System.out.println("└─────────────────────────────────┘");

            int choice = readIntInput("Вибір: ");

            switch (choice) {
                case 1: showDetailedInfo(); break;
                case 2: showCaloriesInfo(); break;
                case 3: showIngredients(); break;
                case 4: showSaladStatistics(); break;
                case 0: return;
                default: System.out.println("❌ Невірний вибір!");
            }
        }
    }

    private void showDetailedInfo() {
        System.out.println("\n" + saladService.getSaladDetails(currentSalad.getName()));
    }

    private void showCaloriesInfo() {
        double calories = saladService.calculateCalories(currentSalad.getName());
        double weight = saladService.calculateWeight(currentSalad.getName());

        System.out.println("\n╔════════════════════════════════════╗");
        System.out.println("║   КАЛОРІЙНІСТЬ САЛАТУ             ║");
        System.out.println("╚════════════════════════════════════╝");
        System.out.printf("Назва:                %s%n", currentSalad.getName());
        System.out.printf("Кількість інгредієнтів: %d%n", currentSalad.getIngredientCount());
        System.out.printf("Загальна вага:        %.1f г%n", weight);
        System.out.printf("Загальна калорійність: %.1f ккал%n", calories);

        if (weight > 0) {
            System.out.printf("Калорійність на 100г: %.1f ккал%n", (calories / weight) * 100);
        }
    }

    private void showSaladStatistics() {
        if (currentSalad.isEmpty()) {
            System.out.println("\n⚠️  Салат порожній!");
            return;
        }

        System.out.println("\n📊 СТАТИСТИКА САЛАТУ");
        System.out.println("═══════════════════════════════════════");

        // Найкалорійніший інгредієнт
        Ingredient maxCal = null;
        double maxCalories = 0;

        for (Ingredient ing : currentSalad.getIngredients()) {
            Vegetable veg = vegetableService.getVegetable(ing.getVegetableName());
            if (veg != null) {
                double cal = (ing.getWeight() / 100.0) * veg.getCaloriesPer100g();
                if (cal > maxCalories) {
                    maxCalories = cal;
                    maxCal = ing;
                }
            }
        }

        if (maxCal != null) {
            System.out.printf("Найкалорійніший: %s (%.1f ккал)%n",
                    maxCal.getVegetableName(), maxCalories);
        }

        // Найважчий інгредієнт
        Ingredient maxWeight = currentSalad.getIngredients().stream()
                .max(Comparator.comparingDouble(Ingredient::getWeight))
                .orElse(null);

        if (maxWeight != null) {
            System.out.printf("Найважчий: %s (%.1f г)%n",
                    maxWeight.getVegetableName(), maxWeight.getWeight());
        }

        // Розподіл за типами
        Map<String, Integer> typeCount = new HashMap<>();
        for (Ingredient ing : currentSalad.getIngredients()) {
            Vegetable veg = vegetableService.getVegetable(ing.getVegetableName());
            if (veg != null) {
                typeCount.put(veg.getType(), typeCount.getOrDefault(veg.getType(), 0) + 1);
            }
        }

        System.out.println("\nРозподіл за типами:");
        typeCount.forEach((type, count) ->
                System.out.printf("  %s: %d%n", type, count));

        System.out.println("═══════════════════════════════════════");
    }

    // ============================================
    // 5. СОРТУВАННЯ ТА ПОШУК
    // ============================================

    private void sortAndSearch() {
        if (!checkActiveSalad()) return;

        while (true) {
            clearScreen();
            System.out.println("\n┌─────────────────────────────────┐");
            System.out.println("│   🔍 СОРТУВАННЯ ТА ПОШУК       │");
            System.out.println("├─────────────────────────────────┤");
            System.out.println("│ 1. Сортувати за вагою           │");
            System.out.println("│ 2. Сортувати за калорійністю    │");
            System.out.println("│ 3. Сортувати за назвою          │");
            System.out.println("│ 4. Знайти за діапазоном калорій │");
            System.out.println("│ 0. Назад                        │");
            System.out.println("└─────────────────────────────────┘");

            int choice = readIntInput("Вибір: ");

            switch (choice) {
                case 1: sortByWeight(); break;
                case 2: sortByCalories(); break;
                case 3: sortByName(); break;
                case 4: findByCalorieRange(); break;
                case 0: return;
                default: System.out.println("❌ Невірний вибір!");
            }
        }
    }

    private void sortByWeight() {
        List<Ingredient> sorted = saladService.sortIngredientsByWeight(currentSalad.getName());

        System.out.println("\n⚖️  ВІДСОРТОВАНО ЗА ВАГОЮ (зростання):");
        System.out.println("═══════════════════════════════════════════════════");
        displayIngredientList(sorted);
    }

    private void sortByCalories() {
        List<Ingredient> sorted = saladService.sortIngredientsByCalories(currentSalad.getName());

        System.out.println("\n🔥 ВІДСОРТОВАНО ЗА КАЛОРІЙНІСТЮ (зростання):");
        System.out.println("═══════════════════════════════════════════════════");
        displayIngredientList(sorted);
    }

    private void sortByName() {
        List<Ingredient> sorted = saladService.sortIngredientsByName(currentSalad.getName());

        System.out.println("\n📋 ВІДСОРТОВАНО ЗА НАЗВОЮ (А-Я):");
        System.out.println("═══════════════════════════════════════════════════");
        displayIngredientList(sorted);
    }

    private void findByCalorieRange() {
        System.out.println("\n🔍 ПОШУК ЗА КАЛОРІЙНІСТЮ");

        double min = readDoubleInput("Мінімальна калорійність (ккал/100г): ");
        double max = readDoubleInput("Максимальна калорійність (ккал/100г): ");

        try {
            List<Ingredient> found = saladService.findIngredientsByCalorieRange(
                    currentSalad.getName(), min, max);

            if (found.isEmpty()) {
                System.out.printf("\n⚠️  Інгредієнти з калорійністю %.1f-%.1f ккал/100г не знайдені.%n",
                        min, max);
            } else {
                System.out.printf("\n✅ Знайдено %d інгредієнт(ів) у діапазоні %.1f-%.1f ккал/100г:%n",
                        found.size(), min, max);
                System.out.println("═══════════════════════════════════════════════════");
                displayIngredientList(found);
            }
        } catch (Exception e) {
            System.out.println("❌ " + e.getMessage());
        }
    }

    private void displayIngredientList(List<Ingredient> ingredients) {
        for (int i = 0; i < ingredients.size(); i++) {
            Ingredient ing = ingredients.get(i);
            Vegetable veg = vegetableService.getVegetable(ing.getVegetableName());

            if (veg != null) {
                double totalCal = (ing.getWeight() / 100.0) * veg.getCaloriesPer100g();
                System.out.printf("  %d. %s: %.1f г, %.1f ккал/100г, загалом: %.1f ккал%n",
                        i + 1, veg.getName(), ing.getWeight(),
                        veg.getCaloriesPer100g(), totalCal);
            }
        }
    }

    private void cleanupOrphanedIngredients() {
        Map<String, List<String>> orphaned = saladService.findOrphanedIngredients();

        if (orphaned.isEmpty()) {
            System.out.println("\n✅ Немає \"мертвих\" інгредієнтів!");
            return;
        }

        System.out.println("\n⚠️  ЗНАЙДЕНО \"МЕРТВІ\" ІНГРЕДІЄНТИ:");
        for (Map.Entry<String, List<String>> entry : orphaned.entrySet()) {
            System.out.printf("Салат '%s': %s%n",
                    entry.getKey(),
                    String.join(", ", entry.getValue()));
        }

        System.out.print("\n🗑️  Видалити всі \"мертві\" інгредієнти? (так/ні): ");
        String confirm = scanner.nextLine().trim().toLowerCase();

        if (confirm.equals("так") || confirm.equals("yes") || confirm.equals("y")) {
            int removed = saladService.cleanupOrphanedIngredients();
            System.out.printf("✅ Видалено %d інгредієнтів!%n", removed);
        } else {
            System.out.println("❌ Скасовано.");
        }
    }
    // ============================================
    // ДОПОМІЖНІ МЕТОДИ
    // ============================================

    private boolean checkActiveSalad() {
        if (currentSalad == null) {
            System.out.println("\n⚠️  Спочатку оберіть активний салат!");
            System.out.println("💡 Перейдіть в 'Управління салатами' -> 'Вибрати активний'");
            return false;
        }
        return true;
    }

    private void loadData() {
        try {
            vegetableService.loadFromFile();
            saladService.loadFromFile();
        } catch (Exception e) {
            System.err.println("⚠️  Помилка завантаження: " + e.getMessage());
        }
    }

    private void saveData() {
        try {
            vegetableService.saveToFile();
            saladService.saveToFile();
            System.out.println("\n✅ Всі дані збережено!");
        } catch (Exception e) {
            System.err.println("❌ Помилка збереження: " + e.getMessage());
        }
    }

    private void saveBeforeExit() {
        System.out.print("\n💾 Зберегти зміни перед виходом? (так/ні): ");
        String answer = scanner.nextLine().trim().toLowerCase();
        if (answer.equals("так") || answer.equals("yes") || answer.equals("y")) {
            saveData();
        }
    }

    private void printWelcome() {
        System.out.println("\n╔════════════════════════════════════╗");
        System.out.println("║   🥗 Шеф-кухар PRO v2.0 🥗       ║");
        System.out.println("║   Професійне управління салатами   ║");
        System.out.println("╚════════════════════════════════════╝");
    }

    private void clearScreen() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }

    private String truncate(String str, int maxLength) {
        if (str == null) return "";
        if (str.length() <= maxLength) return str;
        return str.substring(0, maxLength - 3) + "...";
    }

    private int readIntInput(String prompt) {
        System.out.print(prompt);
        while (!scanner.hasNextInt()) {
            scanner.next();
            System.out.print("⚠️  Введіть ціле число: ");
        }
        int result = scanner.nextInt();
        scanner.nextLine();
        return result;
    }

    private double readDoubleInput(String prompt) {
        System.out.print(prompt);
        while (!scanner.hasNextDouble()) {
            scanner.next();
            System.out.print("⚠️  Введіть число: ");
        }
        double result = scanner.nextDouble();
        scanner.nextLine();
        return result;
    }

    private boolean readBooleanInput() {
        String input = scanner.nextLine().trim().toLowerCase();
        return input.equals("true") || input.equals("так") || input.equals("yes") || input.equals("y");
    }
}