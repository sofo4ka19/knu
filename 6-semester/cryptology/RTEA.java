import java.security.MessageDigest;
import java.util.Scanner;

public class RTEA {
    private static byte[] padding(byte[] input) {
        int originalLength = input.length;

        int newLength = originalLength;
        while (newLength % 8 != 0) {
            newLength++;
        }
        byte[] padded = new byte[newLength];

        System.arraycopy(input, 0, padded, 0, originalLength);
        return padded;
    }
    private static int[] bytesToBits(byte[] padded) {
        int newArrayLength = padded.length/4;
        int[] W = new int[newArrayLength];
        for (int i = 0; i < newArrayLength; i++) {
            W[i] = ((padded[i*4] & 0xFF) << 24) |
                    ((padded[i*4 + 1] & 0xFF) << 16) |
                    ((padded[i*4 + 2] & 0xFF) << 8) |
                    (padded[i*4 + 3] & 0xFF);
        }
        return W;
    }
    private static String bitsToString(int[] W) {
        StringBuilder sb = new StringBuilder();
        for (int j : W) sb.append(String.format("%08x", j));
        return sb.toString();
    }
    private static byte[] bitsToBytes(int[] word) {
        byte[] result = new byte[word.length * 4];
        for (int i = 0; i < result.length; i+=4) {
            result[i] = (byte) (word[i/4] >>> 24);
            result[i+1] = (byte) (word[i/4] >>> 16);
            result[i+2] = (byte) (word[i/4] >>> 8);
            result[i+3] = (byte) (word[i/4]);
        }
        return result;
    }
    private static byte[] unpad(byte[] input) {
        int end = input.length;
        while (end > 0 && input[end - 1] == 0x00) end--;
        byte[] result = new byte[end];
        System.arraycopy(input, 0, result, 0, end);
        return result;
    }
    private static int[] encrypt(byte[] input, byte[] key){
        int[] data = bytesToBits(padding(input));
        int[] keys = bytesToBits(key);
        int keyLength = keys.length;
        for (int i = 0; i < data.length - 1; i+=2) {
            int a = data[i];
            int b = data[i+1];
            for (int r=0; r<32 + keyLength * 4; r++){
                int c=b;
                b+=a+((b<<6)^(b>>>8))+keys[r%keyLength]+r;
                a=c;
            }
            data[i]=a;
            data[i+1]=b;
        }
        return data;
    }
    private static int[] decrypt(byte[] input, byte[] key){
        int[] data = bytesToBits(input);
        int[] keys = bytesToBits(key);
        int keyLength = keys.length;
        for (int i = 0; i < data.length - 1; i+=2) {
            int a = data[i];
            int b = data[i+1];
            for (int r=31 + keyLength * 4; r>=0; r--){
                int c = a;
                a = b - (a + ((a << 6) ^ (a >>> 8)) + keys[r % keyLength] + r);
                b = c;
            }
            data[i]=a;
            data[i+1]=b;
        }
        return data;
    }

    public static void main(String[] args) throws Exception{
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter passphrase: ");
        byte[] passphrase = sc.nextLine().getBytes();
        byte[] derivedKey = MessageDigest.getInstance("SHA-256").digest(passphrase);
        System.out.println("Hashed key (for checking): " + bitsToString(bytesToBits(derivedKey)));
        System.out.print("Enter a word to encrypt: ");
        byte[] input = sc.nextLine().getBytes();
        int[] encrypted = encrypt(input, derivedKey);
        System.out.println("Encrypted value: " + bitsToString(encrypted));
        int[] decrypted = decrypt(bitsToBytes(encrypted), derivedKey);
        System.out.println("Decrypted value: " + bitsToString(decrypted));
        byte[] recovered = unpad(bitsToBytes(decrypted));
        String recoveredText = new String(recovered);
        System.out.println("Decrypted text: " + recoveredText);

        // Correctness check
        boolean match = new String(input).equals(recoveredText);
        System.out.println("\nCorrectness check: original.equals(decrypted) -> " + match);
        if (!match) {
            System.out.println("  original:  [" + new String(input) + "]");
            System.out.println("  recovered: [" + recoveredText + "]");
        }
    }
}
