package com.example.chef.service;

import com.example.chef.model.*;
import com.example.chef.utils.SaladFileHandler;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

public class SaladService {
    private Map<String, Salad> salads; // назва -> салат
    private SaladFileHandler fileHandler;
    private VegetableService vegetableService;

    public SaladService(VegetableService vegetableService) {
        this.salads = new LinkedHashMap<>();
        this.fileHandler = new SaladFileHandler();
        this.vegetableService = vegetableService;
    }

    public SaladService(VegetableService vegetableService, String filePath) {
        this.salads = new LinkedHashMap<>();
        this.fileHandler = new SaladFileHandler(filePath);
        this.vegetableService = vegetableService;
    }

    /**
     * Завантажує салати з файлу.
     */
    public void loadFromFile() throws IOException {
        salads.clear();
        List<Salad> loaded = fileHandler.readAll();

        for (Salad salad : loaded) {
            // Перевіряємо, чи існують всі овочі
            boolean allExist = true;
            for (Ingredient ing : salad.getIngredients()) {
                if (!vegetableService.exists(ing.getVegetableName())) {
                    System.err.printf("⚠️  Овоч '%s' не знайдено в реєстрі%n",
                            ing.getVegetableName());
                    allExist = false;
                }
            }

            if (allExist) {
                salads.put(salad.getName().toLowerCase(), salad);
            }
        }

        System.out.printf("✅ Завантажено %d салатів%n", salads.size());
    }

    /**
     * Зберігає салати у файл.
     */
    public void saveToFile() throws IOException {
        fileHandler.writeAll(salads.values());
        System.out.printf("✅ Збережено %d салатів%n", salads.size());
    }

    /**
     * Створює новий салат (без дублікатів).
     */
    public boolean createSalad(Salad salad) {
        String key = salad.getName().toLowerCase();

        if (salads.containsKey(key)) {
            return false; // дублікат
        }

        salads.put(key, salad);
        return true;
    }

    /**
     * Отримує салат за назвою.
     */
    public Salad getSalad(String name) {
        return salads.get(name.toLowerCase());
    }

    /**
     * Видаляє салат.
     */
    public boolean deleteSalad(String name) {
        return salads.remove(name.toLowerCase()) != null;
    }

    /**
     * Перейменовує салат.
     */
    public boolean renameSalad(String oldName, String newName) {
        String oldKey = oldName.toLowerCase();
        String newKey = newName.toLowerCase();

        if (!salads.containsKey(oldKey)) {
            return false;
        }

        if (!oldKey.equals(newKey) && salads.containsKey(newKey)) {
            return false; // нова назва вже існує
        }

        Salad salad = salads.remove(oldKey);
        salad.setName(newName);
        salads.put(newKey, salad);
        return true;
    }

    /**
     * Перевіряє існування салату.
     */
    public boolean exists(String name) {
        return salads.containsKey(name.toLowerCase());
    }

    /**
     * Додає інгредієнт до салату (з перевіркою овочу).
     */
    public boolean addIngredient(String saladName, String vegetableName, double weight) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return false;
        }

        if (!vegetableService.exists(vegetableName)) {
            System.err.printf("⚠️  Овоч '%s' не знайдено в реєстрі%n", vegetableName);
            return false;
        }

        salad.addIngredient(vegetableName, weight);
        return true;
    }

    /**
     * Обчислює калорійність салату.
     */
    public double calculateCalories(String saladName) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return 0;
        }

        double totalCalories = 0;
        for (Ingredient ing : salad.getIngredients()) {
            Vegetable veg = vegetableService.getVegetable(ing.getVegetableName());
            if (veg != null) {
                totalCalories += (ing.getWeight() / 100.0) * veg.getCaloriesPer100g();
            }
        }

        return totalCalories;
    }

    /**
     * Обчислює вагу салату.
     */
    public double calculateWeight(String saladName) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return 0;
        }

        return salad.getIngredients().stream()
                .mapToDouble(Ingredient::getWeight)
                .sum();
    }

    /**
     * Повертає всі салати.
     */
    public Collection<Salad> getAllSalads() {
        return new ArrayList<>(salads.values());
    }

    /**
     * Повертає список назв салатів.
     */
    public List<String> getSaladNames() {
        return new ArrayList<>(salads.keySet());
    }

    /**
     * Повертає кількість салатів.
     */
    public int getCount() {
        return salads.size();
    }

    /**
     * Очищає всі салати.
     */
    public void clear() {
        salads.clear();
    }

    /**
     * Сортує інгредієнти салату за вагою.
     */
    public List<Ingredient> sortIngredientsByWeight(String saladName) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return new ArrayList<>();
        }

        return salad.getIngredients().stream()
                .sorted(Comparator.comparingDouble(Ingredient::getWeight))
                .collect(Collectors.toList());
    }

    /**
     * Сортує інгредієнти за калорійністю.
     */
    public List<Ingredient> sortIngredientsByCalories(String saladName) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return new ArrayList<>();
        }

        return salad.getIngredients().stream()
                .sorted((i1, i2) -> {
                    Vegetable v1 = vegetableService.getVegetable(i1.getVegetableName());
                    Vegetable v2 = vegetableService.getVegetable(i2.getVegetableName());
                    if (v1 == null || v2 == null) return 0;
                    return Double.compare(v1.getCaloriesPer100g(), v2.getCaloriesPer100g());
                })
                .collect(Collectors.toList());
    }
    /**
     * Сортує інгредієнти за назваою.
     */
    public List<Ingredient> sortIngredientsByName(String saladName) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return new ArrayList<>();
        }

        return salad.getIngredients().stream()
                .filter(i -> vegetableService.getVegetable(i.getVegetableName()) != null)
                .sorted(Comparator.comparing(
                        i -> vegetableService.getVegetable(i.getVegetableName()).getName(),
                        String.CASE_INSENSITIVE_ORDER
                ))
                .collect(Collectors.toList());
    }

    /**
     * Шукає інгредієнти за діапазоном калорійності.
     */
    public List<Ingredient> findIngredientsByCalorieRange(String saladName,
                                                          double min, double max) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return new ArrayList<>();
        }

        return salad.getIngredients().stream()
                .filter(ing -> {
                    Vegetable veg = vegetableService.getVegetable(ing.getVegetableName());
                    if (veg == null) return false;
                    double cal = veg.getCaloriesPer100g();
                    return cal >= min && cal <= max;
                })
                .collect(Collectors.toList());
    }

    /**
     * Знаходить всі салати, що використовують вказаний овоч.
     */
    public List<String> findSaladsUsingVegetable(String vegetableName) {
        List<String> result = new ArrayList<>();

        for (Salad salad : salads.values()) {
            if (salad.hasIngredient(vegetableName)) {
                result.add(salad.getName());
            }
        }

        return result;
    }

    /**
     * Оновлює назву овочу у всіх салатах.
     */
    public void updateVegetableNameInAllSalads(String oldName, String newName) {
        for (Salad salad : salads.values()) {
            for (Ingredient ingredient : salad.getIngredients()) {
                if (ingredient.getVegetableName().equalsIgnoreCase(oldName)) {
                    // Видаляємо старий
                    salad.removeIngredient(oldName);
                    // Додаємо з новою назвою
                    salad.addIngredient(newName, ingredient.getWeight());
                }
            }
        }
    }

    /**
     * Повертає детальну інформацію про салат.
     */
    public String getSaladDetails(String saladName) {
        Salad salad = getSalad(saladName);
        if (salad == null) {
            return "Салат не знайдено";
        }

        StringBuilder sb = new StringBuilder();
        sb.append("═══════════════════════════════════════\n");
        sb.append(String.format("  Салат '%s'\n", salad.getName()));
        sb.append("═══════════════════════════════════════\n");
        sb.append("Інгредієнти:\n");

        int index = 1;
        for (Ingredient ing : salad.getIngredients()) {
            Vegetable veg = vegetableService.getVegetable(ing.getVegetableName());
            if (veg != null) {
                double totalCal = (ing.getWeight() / 100.0) * veg.getCaloriesPer100g();
                sb.append(String.format("  %d. %s (%s): %.1f г, %.1f ккал/100г, загалом: %.1f ккал\n",
                        index++, veg.getName(), veg.getType(),
                        ing.getWeight(), veg.getCaloriesPer100g(), totalCal));
            }
        }

        sb.append("───────────────────────────────────────\n");
        sb.append(String.format("Загальна вага:        %.1f г\n", calculateWeight(saladName)));
        sb.append(String.format("Загальна калорійність: %.1f ккал\n", calculateCalories(saladName)));
        sb.append("═══════════════════════════════════════\n");

        return sb.toString();
    }
}

