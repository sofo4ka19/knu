package com.example.chef.service;

import com.example.chef.model.*;
import com.example.chef.utils.VegetableFileHandler;
import java.io.IOException;
import java.util.*;

public class VegetableService {
    private Map<String, Vegetable> vegetables; // назва -> овоч
    private VegetableFileHandler fileHandler;
    private SaladService saladService; // для перевірки використання

    public VegetableService() {
        this.vegetables = new LinkedHashMap<>();
        this.fileHandler = new VegetableFileHandler();
    }

    public VegetableService(String filePath) {
        this.vegetables = new LinkedHashMap<>();
        this.fileHandler = new VegetableFileHandler(filePath);
    }
    /**
     * Встановлює зв'язок з SaladService для перевірки використання овочів.
     */
    public void setSaladService(SaladService saladService) {
        this.saladService = saladService;
    }

    /**
     * Завантажує овочі з файлу.
     */
    public void loadFromFile() throws IOException {
        vegetables.clear();
        List<Vegetable> loaded = fileHandler.readAll();

        for (Vegetable veg : loaded) {
            vegetables.put(veg.getName().toLowerCase(), veg);
        }

        System.out.printf("✅ Завантажено %d овочів%n", vegetables.size());
    }

    /**
     * Зберігає овочі у файл.
     */
    public void saveToFile() throws IOException {
        fileHandler.writeAll(vegetables.values());
        System.out.printf("✅ Збережено %d овочів%n", vegetables.size());
    }

    /**
     * Додає новий овоч (без дублікатів).
     */
    public boolean addVegetable(Vegetable vegetable) {
        String key = vegetable.getName().toLowerCase();

        if (vegetables.containsKey(key)) {
            return false; // дублікат
        }

        vegetables.put(key, vegetable);
        return true;
    }

    /**
     * Отримує овоч за назвою (регістр не важливий).
     */
    public Vegetable getVegetable(String name) {
        return vegetables.get(name.toLowerCase());
    }

    /**
     * Видаляє овоч, але ТІЛЬКИ якщо він не використовується в салатах.
     *
     * @return true якщо видалено, false якщо використовується
     * @throws IllegalStateException якщо овоч використовується
     */
    public boolean deleteVegetable(String name) {
        if (!exists(name)) {
            return false;
        }

        // Перевіряємо чи використовується овоч
        if (saladService != null) {
            List<String> usedIn = saladService.findSaladsUsingVegetable(name);
            if (!usedIn.isEmpty()) {
                throw new IllegalStateException(
                        "Неможливо видалити овоч '" + name + "'. " +
                                "Він використовується в салатах: " + String.join(", ", usedIn)
                );
            }
        }

        return vegetables.remove(name.toLowerCase()) != null;
    }


    /**
     * Оновлює параметри овочу.
     */
    public boolean updateVegetable(String oldName, Vegetable newVegetable) {
        String oldKey = oldName.toLowerCase();
        String newKey = newVegetable.getName().toLowerCase();

        if (!vegetables.containsKey(oldKey)) {
            return false; // овоч не знайдено
        }

        // Якщо змінюється назва, перевіряємо дублікат
        if (!oldKey.equals(newKey) && vegetables.containsKey(newKey)) {
            return false; // нова назва вже існує
        }

        vegetables.remove(oldKey);
        vegetables.put(newKey, newVegetable);
        return true;
    }
    /**
     * Оновлює назву овочу та автоматично оновлює всі салати.
     */
    public boolean updateVegetableName(String oldName, String newName) {
        String oldKey = oldName.toLowerCase();
        String newKey = newName.toLowerCase();

        if (!vegetables.containsKey(oldKey)) {
            return false;
        }

        if (!oldKey.equals(newKey) && vegetables.containsKey(newKey)) {
            throw new IllegalArgumentException("Овоч з назвою '" + newName + "' вже існує");
        }

        Vegetable vegetable = vegetables.get(oldKey);
        vegetable.setName(newName);

        vegetables.remove(oldKey);
        vegetables.put(newKey, vegetable);

        // Оновлюємо всі салати
        if (saladService != null && !oldName.equalsIgnoreCase(newName)) {
            saladService.updateVegetableNameInAllSalads(oldName, newName);
        }

        return true;
    }

    /**
     * Перевіряє чи використовується овоч у салатах.
     */
    public boolean isVegetableUsed(String name) {
        if (saladService == null) {
            return false;
        }
        return !saladService.findSaladsUsingVegetable(name).isEmpty();
    }

    /**
     * Повертає список салатів, де використовується овоч.
     */
    public List<String> getUsageInfo(String name) {
        if (saladService == null) {
            return new ArrayList<>();
        }
        return saladService.findSaladsUsingVegetable(name);
    }

    /**
     * Перевіряє існування овочу.
     */
    public boolean exists(String name) {
        return vegetables.containsKey(name.toLowerCase());
    }

    /**
     * Повертає всі овочі.
     */
    public Collection<Vegetable> getAllVegetables() {
        return new ArrayList<>(vegetables.values());
    }

    /**
     * Повертає список назв овочів.
     */
    public List<String> getVegetableNames() {
        return new ArrayList<>(vegetables.keySet());
    }

    /**
     * Повертає кількість овочів.
     */
    public int getCount() {
        return vegetables.size();
    }

    /**
     * Очищає реєстр овочів.
     */
    public void clear() {
        vegetables.clear();
    }

    /**
     * Шукає овочі за типом.
     */
    public List<Vegetable> findByType(String type) {
        return vegetables.values().stream()
                .filter(v -> v.getType().equalsIgnoreCase(type))
                .toList();
    }

    /**
     * Сортує овочі за назвою.
     */
    public List<Vegetable> sortByName() {
        return vegetables.values().stream()
                .sorted(Comparator.comparing(Vegetable::getName))
                .toList();
    }

    /**
     * Сортує овочі за калорійністю.
     */
    public List<Vegetable> sortByCalories() {
        return vegetables.values().stream()
                .sorted(Comparator.comparingDouble(Vegetable::getCaloriesPer100g))
                .toList();
    }

    /**
     * Шукає овочі в діапазоні калорійності.
     */
    public List<Vegetable> findByCalorieRange(double min, double max) {
        if (min < 0 || max < 0 || min > max) {
            throw new IllegalArgumentException("Некоректний діапазон калорійності");
        }

        return vegetables.values().stream()
                .filter(v -> v.getCaloriesPer100g() >= min && v.getCaloriesPer100g() <= max)
                .toList();
    }
}
