import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.NoSuchFileException;
import java.nio.file.Path;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        String filePath = args.length > 0 ? args[0] : "example.scala";
        Path path = Path.of(filePath);

        String src;
        try {
            src = Files.readString(path);
        } catch (NoSuchFileException e) {
            System.err.println("Error: file not found: " + filePath);
            return;
        } catch (IOException e) {
            System.err.println("Error: could not read file: " + filePath + " — " + e.getMessage());
            return;
        }

        if (src.isBlank()) {
            System.err.println("Warning: file is empty: " + filePath);
            return;
        }

        Scanner scanner = new Scanner(src);
        List<TokenInfo> tokens = scanner.tokenize();

        System.out.printf("%-12s %-15s %s%n", "[line:col]", "TOKEN", "VALUE");
        System.out.println("-".repeat(50));
        for (TokenInfo t : tokens) {
            System.out.println(t);
        }
    }
}