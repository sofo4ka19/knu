import java.util.ArrayList;
import java.util.List;
import java.util.Set;

public class Scanner {

    private static final Set<String> KEYWORDS = Set.of(
            "abstract", "case", "class", "def", "do", "else", "extends",
            "false", "final", "for", "if", "import", "lazy", "match", "new",
            "null", "object", "override", "package", "private", "protected",
            "return", "sealed", "super", "this", "throw", "trait", "true",
            "try", "type", "val", "var", "while", "with", "yield"
    );

    //the tokens after which the implicit SEMI may be added
    private static final Set<Token> SEMI_AFTER = Set.of(
            Token.IDENTIFIER, Token.INTLIT, Token.FLOATLIT,
            Token.STRINGLIT, Token.CHARLIT,
            Token.THIS, Token.NULL, Token.TRUE, Token.FALSE, Token.RETURN, Token.TYPE,
            Token.RPAREN, Token.RBRACKET, Token.RBRACE
    );

    private final String src;
    private int pos;
    private int line;
    private int col;

    private Token lastToken;
    //used for ignoring adding SEMI inside () or []
    private int parenDepth;

    public Scanner(String src) {
        this.src        = src;
        this.pos        = 0;
        this.line       = 1;
        this.col        = 1;
        this.lastToken  = null;
        this.parenDepth = 0;
    }

    public List<TokenInfo> tokenize() {
        List<TokenInfo> result = new ArrayList<>();

        while (pos < src.length()) {
            char c = src.charAt(pos);

            //handling new line
            if (c == '\n') {
                if (lastToken != null && SEMI_AFTER.contains(lastToken) && parenDepth == 0) {
                    result.add(new TokenInfo(Token.SEMI, "\n", line, col));
                    lastToken = Token.SEMI;
                }
                advance();
                continue;
            }

            if (Character.isWhitespace(c)) {
                advance();
                continue;
            }

            //handling comments
            if (c == '/' && pos + 1 < src.length()) {
                char next = src.charAt(pos + 1);
                if (next == '/') {
                    result.add(readLineComment());
                    continue;
                }
                if (next == '*') {
                    result.add(readBlockComment());
                    continue;
                }
            }

            //handling string literals
            if (c == '"') {
                result.add(readString());
                continue;
            }

            //handling char literals
            if (c == '\'') {
                result.add(readChar());
                continue;
            }

            //handling numbers
            if (Character.isDigit(c)) {
                result.add(readNumber());
                continue;
            }

            //handling identifiers and keywords
            if (Character.isLetter(c) || c == '_') {
                result.add(readIdentOrKeyword());
                continue;
            }

            //handling symbols and operators
            TokenInfo t = readSymbol();
            if (t != null) {
                result.add(t);
            } else {
                System.err.println("Warning: unknown character '" + c
                        + "' (U+" + String.format("%04X", (int) c)
                        + ") at line " + line + ", col " + col + " — skipping");
                advance();
            }
        }

        if (lastToken != null && SEMI_AFTER.contains(lastToken) && parenDepth == 0) {
            result.add(new TokenInfo(Token.SEMI, "\n", line, col));
        }

        result.add(new TokenInfo(Token.EOF, "<EOF>", line, col));
        return result;
    }

    private TokenInfo readIdentOrKeyword() {
        int startLine = line, startCol = col;
        StringBuilder sb = new StringBuilder();
        while (pos < src.length()) {
            char c = src.charAt(pos);
            if (Character.isLetterOrDigit(c) || c == '_') {
                sb.append(c);
                advance();
            } else {
                break;
            }
        }
        String word = sb.toString();
        Token tok = KEYWORDS.contains(word)
                ? Token.valueOf(word.toUpperCase())
                : Token.IDENTIFIER;
        lastToken = tok;
        return new TokenInfo(tok, word, startLine, startCol);
    }

    private TokenInfo readNumber() {
        int startLine = line, startCol = col;
        StringBuilder sb = new StringBuilder();
        boolean isFloat = false;
        while (pos < src.length()) {
            char c = src.charAt(pos);
            if (Character.isDigit(c)) {
                sb.append(c);
                advance();
            } else if (c == '.' && !isFloat
                    && pos + 1 < src.length()
                    && Character.isDigit(src.charAt(pos + 1))) {
                isFloat = true;
                sb.append(c);
                advance();
            } else {
                break;
            }
        }
        Token tok = isFloat ? Token.FLOATLIT : Token.INTLIT;
        lastToken = tok;
        return new TokenInfo(tok, sb.toString(), startLine, startCol);
    }

    private TokenInfo readString() {
        int startLine = line, startCol = col;
        StringBuilder sb = new StringBuilder();
        boolean closed = false;
        advance();
        while (pos < src.length()) {
            char c = src.charAt(pos);
            if (c == '\\' && pos + 1 < src.length()) {
                sb.append(c); advance();
                sb.append(src.charAt(pos)); advance();
            } else if (c == '"') {
                advance();
                closed = true;
                break;
            } else if (c == '\n') {
                break;
            } else {
                sb.append(c); advance();
            }
        }
        if (!closed) {
            System.err.println("Warning: unterminated string literal at line " + startLine);
        }
        lastToken = Token.STRINGLIT;
        return new TokenInfo(Token.STRINGLIT, "\"" + sb + "\"", startLine, startCol);
    }

    private TokenInfo readChar() {
        int startLine = line, startCol = col;
        StringBuilder sb = new StringBuilder();
        boolean closed = false;
        advance();
        while (pos < src.length()) {
            char c = src.charAt(pos);
            if (c == '\\' && pos + 1 < src.length()) {
                sb.append(c); advance();
                sb.append(src.charAt(pos)); advance();
            } else if (c == '\'') {
                advance();
                closed = true;
                break;
            } else if (c == '\n') {
                break;
            } else {
                sb.append(c); advance();
            }
        }
        String content = sb.toString();
        if (!closed) {
            System.err.println("Warning: unterminated char literal at line " + startLine);
        } else if (content.isEmpty()) {
            System.err.println("Warning: empty char literal at line "
                    + startLine + ", col " + startCol);
        } else if (!content.startsWith("\\") && content.length() != 1) {
            System.err.println("Warning: invalid char literal '" + content
                    + "' at line " + startLine + ", col " + startCol);
        }
        lastToken = Token.CHARLIT;
        return new TokenInfo(Token.CHARLIT, "'" + content + "'", startLine, startCol);
    }

    private TokenInfo readSymbol() {
        int startLine = line, startCol = col;
        char c = src.charAt(pos);
        advance();

        Token tok = switch (c) {
            case '(' -> Token.LPAREN;
            case ')' -> Token.RPAREN;
            case '[' -> Token.LBRACKET;
            case ']' -> Token.RBRACKET;
            case '{' -> Token.LBRACE;
            case '}' -> Token.RBRACE;
            case '=' -> Token.ASSIGN;
            case '+' -> Token.PLUS;
            case '-' -> Token.MINUS;
            case '!' -> Token.BANG;
            case '~' -> Token.TILDE;
            case ',' -> Token.COMMA;
            case '.' -> Token.DOT;
            case ':' -> Token.COLON;
            case ';' -> Token.SEMI;
            default  -> null;
        };

        if (tok == null) return null;

        switch (tok) {
            case LPAREN, LBRACKET -> parenDepth++;
            case RPAREN, RBRACKET -> parenDepth = Math.max(0, parenDepth - 1);
            default -> {}
        }

        lastToken = tok;
        return new TokenInfo(tok, String.valueOf(c), startLine, startCol);
    }

    private TokenInfo readLineComment() {
        int startLine = line, startCol = col;
        StringBuilder sb = new StringBuilder();
        sb.append(src.charAt(pos)); advance(); // '/'
        sb.append(src.charAt(pos)); advance(); // '/'
        while (pos < src.length() && src.charAt(pos) != '\n') {
            sb.append(src.charAt(pos));
            advance();
        }
        return new TokenInfo(Token.LINECOMMENT, sb.toString(), startLine, startCol);
    }

    private TokenInfo readBlockComment() {
        int startLine = line, startCol = col;
        StringBuilder sb = new StringBuilder();
        sb.append(src.charAt(pos)); advance(); // '/'
        sb.append(src.charAt(pos)); advance(); // '*'
        while (pos + 1 < src.length()) {
            if (src.charAt(pos) == '*' && src.charAt(pos + 1) == '/') {
                sb.append(src.charAt(pos)); advance();
                sb.append(src.charAt(pos)); advance();
                return new TokenInfo(Token.BLOCKCOMMENT, sb.toString(), startLine, startCol);
            }
            sb.append(src.charAt(pos));
            advance();
        }
        while (pos < src.length()) {
            sb.append(src.charAt(pos));
            advance();
        }
        System.err.println("Warning: unterminated block comment starting at line " + startLine);
        return new TokenInfo(Token.BLOCKCOMMENT, sb.toString(), startLine, startCol);
    }

    private void advance() {
        if (pos < src.length() && src.charAt(pos) == '\n') {
            line++;
            col = 1;
        } else {
            col++;
        }
        pos++;
    }
}