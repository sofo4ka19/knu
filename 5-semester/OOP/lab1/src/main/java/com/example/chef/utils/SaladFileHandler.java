package com.example.chef.utils;

import com.example.chef.model.*;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class SaladFileHandler {
    private static final String DEFAULT_PATH = "data/salads.csv";
    private String filePath;

    public SaladFileHandler() {
        this(DEFAULT_PATH);
    }

    public SaladFileHandler(String filePath) {
        this.filePath = filePath;
        ensureFileExists();
    }

    private void ensureFileExists() {
        try {
            Path path = Paths.get(filePath);
            if (!Files.exists(path)) {
                Files.createDirectories(path.getParent());
                Files.createFile(path);
                writeHeader();
            }
        } catch (IOException e) {
            System.err.println("Помилка створення файлу: " + e.getMessage());
        }
    }

    private void writeHeader() throws IOException {
        String header = "# Збережені салати\n" +
                "# Формат:\n" +
                "# SALAD;назва_салату\n" +
                "# INGREDIENT;назва_овочу;вага\n" +
                "# (порожній рядок між салатами)\n";

        Files.write(Paths.get(filePath),
                header.getBytes(StandardCharsets.UTF_8));
    }

    /**
     * Читає всі салати з файлу.
     */
    public List<Salad> readAll() throws IOException {
        List<Salad> salads = new ArrayList<>();

        if (!Files.exists(Paths.get(filePath))) {
            return salads;
        }

        List<String> lines = Files.readAllLines(Paths.get(filePath), StandardCharsets.UTF_8);
        Salad currentSalad = null;

        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i).trim();

            if (line.isEmpty() || line.startsWith("#")) {
                continue;
            }

            try {
                if (line.startsWith("SALAD;")) {
                    // Новий салат
                    if (currentSalad != null) {
                        salads.add(currentSalad);
                    }
                    String saladName = line.substring(6).trim();
                    currentSalad = new Salad(saladName);

                } else if (line.startsWith("INGREDIENT;") && currentSalad != null) {
                    // Інгредієнт
                    String[] parts = line.substring(11).split(";");
                    if (parts.length >= 2) {
                        String vegName = parts[0].trim();
                        double weight = Double.parseDouble(parts[1].trim());
                        currentSalad.addIngredient(vegName, weight);
                    }
                }
            } catch (Exception e) {
                System.err.printf("Помилка в рядку %d: %s%n", i + 1, e.getMessage());
            }
        }

        // Додаємо останній салат
        if (currentSalad != null) {
            salads.add(currentSalad);
        }

        return salads;
    }

    /**
     * Записує всі салати у файл.
     */
    public void writeAll(Collection<Salad> salads) throws IOException {
        List<String> lines = new ArrayList<>();

        for (Salad salad : salads) {
            lines.add("SALAD;" + salad.getName());

            for (Ingredient ingredient : salad.getIngredients()) {
                lines.add("INGREDIENT;" + ingredient.toFileString());
            }

            lines.add(""); // порожній рядок між салатами
        }

        Files.write(Paths.get(filePath),
                lines,
                StandardCharsets.UTF_8,
                StandardOpenOption.CREATE,
                StandardOpenOption.TRUNCATE_EXISTING);
    }

    /**
     * Додає новий салат до файлу.
     */
    public void append(Salad salad) throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append("SALAD;").append(salad.getName()).append("\n");

        for (Ingredient ingredient : salad.getIngredients()) {
            sb.append("INGREDIENT;").append(ingredient.toFileString()).append("\n");
        }

        sb.append("\n");

        Files.write(Paths.get(filePath),
                sb.toString().getBytes(StandardCharsets.UTF_8),
                StandardOpenOption.CREATE,
                StandardOpenOption.APPEND);
    }

    /**
     * Видаляє салат з файлу за назвою.
     */
    public boolean delete(String saladName) throws IOException {
        List<Salad> salads = readAll();
        boolean removed = salads.removeIf(s -> s.getName().equalsIgnoreCase(saladName));

        if (removed) {
            writeAll(salads);
        }

        return removed;
    }

    /**
     * Оновлює салат у файлі.
     */
    public boolean update(Salad salad) throws IOException {
        List<Salad> salads = readAll();
        boolean updated = false;

        for (int i = 0; i < salads.size(); i++) {
            if (salads.get(i).getName().equalsIgnoreCase(salad.getName())) {
                salads.set(i, salad);
                updated = true;
                break;
            }
        }

        if (updated) {
            writeAll(salads);
        }

        return updated;
    }
}
