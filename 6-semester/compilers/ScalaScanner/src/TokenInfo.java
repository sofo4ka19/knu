public class TokenInfo {
    public final Token token;
    public final String value;
    public final int line;
    public final int col;

    public TokenInfo(Token token, String value, int line, int col) {
        this.token = token;
        this.value  = value;
        this.line   = line;
        this.col    = col;
    }

    @Override
    public String toString() {
        String display = token == Token.SEMI && value.equals("\n")
                ? "<newline>"
                : value;
        return String.format("[%3d:%3d]  %-15s %s", line, col, token, display);
    }
}