package com.example.chef.utils;

import com.example.chef.vegetables.*;

import java.io.IOException;

public class VegetableFileHandler extends FileManager<Vegetable> {
    private static final String DEFAULT_PATH = "data/vegetables.csv";

    public VegetableFileHandler() {
        super(DEFAULT_PATH);
    }

    public VegetableFileHandler(String filePath) {
        super(filePath);
    }

    @Override
    protected void writeHeader() throws IOException {
        String header = "# Реєстр овочів\n" +
                "# Формат: тип;назва;калорії;параметр1;параметр2\n" +
                "# ROOT - коренеплід (параметр1: потребує_очищення, параметр2: колір)\n" +
                "# LEAF - листовий (параметр1: тип_листя, параметр2: хрусткий)\n" +
                "# FRUIT - плодовий (параметр1: колір, параметр2: має_насіння)\n";

        java.nio.file.Files.write(
                java.nio.file.Paths.get(filePath),
                header.getBytes(java.nio.charset.StandardCharsets.UTF_8)
        );
    }

    @Override
    protected Vegetable parseLine(String line) throws Exception {
        String[] parts = line.split(";");

        if (parts.length < 5) {
            throw new IllegalArgumentException("Недостатньо параметрів");
        }

        String type = parts[0].trim().toUpperCase();
        String name = parts[1].trim();
        double calories = Double.parseDouble(parts[2].trim());
        String param1 = parts[3].trim();
        String param2 = parts[4].trim();

        switch (type) {
            case "ROOT":
                return new RootVegetable(name, calories, param2);

            case "LEAF":
                boolean isCrispy = Boolean.parseBoolean(param2);
                return new LeafVegetable(name, calories, param1, isCrispy);

            case "FRUIT":
                boolean hasSeed = Boolean.parseBoolean(param2);
                return new FruitVegetable(name, calories, param1, hasSeed);

            default:
                throw new IllegalArgumentException("Невідомий тип: " + type);
        }
    }

    @Override
    protected String toFileLine(Vegetable vegetable) {
        return vegetable.toFileString();
    }
}
