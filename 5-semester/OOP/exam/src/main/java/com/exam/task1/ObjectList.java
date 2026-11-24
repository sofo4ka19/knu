package com.exam.task1;
import java.io.*;
import java.util.*;

public class ObjectList {
    public static void execute() throws IOException {
        List<ObjectItem> list = new ArrayList<>();

        // Читання з файлу та генерація унікальних шифрів
        BufferedReader br = new BufferedReader(new FileReader("objects.txt"));
        String line;
        Set<Integer> usedCodes = new HashSet<>();
        Random rand = new Random();
        while ((line = br.readLine()) != null) {
            int code;
            do {
                code = rand.nextInt(100) + 1; // від 1 до 100
            } while (!usedCodes.add(code)); // повторюємо поки не знайдемо унікальний

            list.add(new ObjectItem(line.trim(), code));
        }
        br.close();


        System.out.println("Початковий список:");
        for (ObjectItem item : list) {
            System.out.println(item);
        }

        // Сортування за шифрами (зростання)
        list.sort((a, b) -> a.code - b.code);

        System.out.println("\nВідсортований за шифрами:");
        for (ObjectItem item : list) {
            System.out.println(item);
        }

        // Видалення дублікатів назв
        Set<String> seen = new HashSet<>();
        list.removeIf(item -> !seen.add(item.name));

        System.out.println("\nПісля видалення дублікатів:");
        for (ObjectItem item : list) {
            System.out.println(item);
        }
    }
}
