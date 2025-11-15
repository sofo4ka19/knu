package com.example.chef.utils;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public abstract class FileManager<T> {
    protected String filePath;

    public FileManager(String filePath) {
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

    protected abstract void writeHeader() throws IOException;
    protected abstract T parseLine(String line) throws Exception;
    protected abstract String toFileLine(T item);

    public List<T> readAll() throws IOException {
        List<T> items = new ArrayList<>();

        if (!Files.exists(Paths.get(filePath))) {
            return items;
        }

        List<String> lines = Files.readAllLines(Paths.get(filePath), StandardCharsets.UTF_8);

        for (int i = 0; i < lines.size(); i++) {
            String line = lines.get(i).trim();

            if (line.isEmpty() || line.startsWith("#")) {
                continue;
            }

            try {
                T item = parseLine(line);
                if (item != null) {
                    items.add(item);
                }
            } catch (Exception e) {
                System.err.printf("Помилка в рядку %d: %s%n", i + 1, e.getMessage());
                System.err.printf("  Рядок: %s%n", line);
            }
        }

        return items;
    }

    public void writeAll(Collection<T> items) throws IOException {
        List<String> lines = new ArrayList<>();

        for (T item : items) {
            lines.add(toFileLine(item));
        }

        Files.write(Paths.get(filePath),
                lines,
                StandardCharsets.UTF_8,
                StandardOpenOption.CREATE,
                StandardOpenOption.TRUNCATE_EXISTING);
    }

    public void append(T item) throws IOException {
        String line = toFileLine(item) + System.lineSeparator();
        Files.write(Paths.get(filePath),
                line.getBytes(StandardCharsets.UTF_8),
                StandardOpenOption.CREATE,
                StandardOpenOption.APPEND);
    }
}
