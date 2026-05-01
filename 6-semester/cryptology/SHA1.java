import java.security.MessageDigest;
import java.util.Scanner;

public class SHA1 {
    static byte[] padding(byte[] input) {
        int originalLength = input.length;

        int newLength = originalLength + 1;
        while (newLength % 64 != 56) {
            newLength++;
        }

        byte[] padded = new byte[newLength + 8];

        System.arraycopy(input, 0, padded, 0, originalLength);

        padded[originalLength] = (byte) 0x80;

        long bitLength = (long) originalLength * 8;

        for (int i = 0; i < 8; i++) {
            padded[padded.length - 8 + i] =
                    (byte) (bitLength >>> (56 - 8 * i));
        }

        return padded;
    }

    static String hash(byte[] input) {
        int h0 = 0x67452301;
        int h1 = 0xEFCDAB89;
        int h2 = 0x98BADCFE;
        int h3 = 0x10325476;
        int h4 = 0xC3D2E1F0;
        byte[] padded = padding(input);

        for (int j = 0; j < padded.length; j+=64) {
            int[] W = new int[80];
            for (int i = 0; i < 16; i++) {
                W[i] = ((padded[i*4] & 0xFF) << 24) |
                        ((padded[i*4 + 1] & 0xFF) << 16) |
                        ((padded[i*4 + 2] & 0xFF) << 8) |
                        (padded[i*4 + 3] & 0xFF);
            }
            for (int i = 16; i < 80; i++) {
                int v = W[i-3]^W[i-8]^W[i-14]^W[i-16];
                W[i]=(v << 1) | (v >>> 31);
            }
            int a = h0;
            int b = h1;
            int c = h2;
            int d = h3;
            int e = h4;

            for (int i = 0; i < 80; i++) {
                int f, k;
                if (i<=19) {
                    f = (b&c)|((~b)&d);
                    k = 0x5A827999;
                } else if (i<=39) {
                    f=b^c^d;
                    k = 0x6ED9EBA1;
                } else if (i<=59) {
                    f=(b&c)|(b&d)|(c&d);
                    k = 0x8F1BBCDC;
                } else {
                    f=b^c^d;
                    k = 0xCA62C1D6;
                }
                int temp = ((a<<5)|(a>>>27))+f+e+k+W[i];
                e=d;
                d=c;
                c=(b<<30)|(b>>>2);
                b=a;
                a=temp;
            }
            h0 = h0 + a;
            h1 = h1 + b;
            h2 = h2 + c;
            h3 = h3 + d;
            h4 = h4 + e;
        }
        return String.format("%08x%08x%08x%08x%08x", h0, h1, h2, h3, h4);
    }

    static String sha1_pr(byte[] input) throws Exception{
        MessageDigest md = MessageDigest.getInstance("SHA-1");
        byte[] result = md.digest(input);
        StringBuilder sb = new StringBuilder();
        for (byte b : result)
            sb.append(String.format("%02x", b & 0xFF));
        return sb.toString();
    }
    public static void main(String[] args) throws Exception{
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter a word to hash: ");
        byte[] input = sc.nextLine().getBytes();

        System.out.println("My result: " + hash(input));
        System.out.println("Reference: " + sha1_pr(input));
    }
}
