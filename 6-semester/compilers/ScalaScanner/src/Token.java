public enum Token {
    // literals
    IDENTIFIER,
    INTLIT,
    FLOATLIT,
    STRINGLIT,
    CHARLIT,

    // keywords
    ABSTRACT, CASE, CLASS, DEF, DO, ELSE, EXTENDS, FALSE, FINAL,
    FOR, IF, IMPORT, LAZY, MATCH, NEW, NULL, OBJECT, OVERRIDE,
    PACKAGE, PRIVATE, PROTECTED, RETURN, SEALED, SUPER, THIS,
    THROW, TRAIT, TRUE, TRY, TYPE, VAL, VAR, WHILE, WITH, YIELD,

    // brackets
    LPAREN,    // (
    RPAREN,    // )
    LBRACKET,  // [
    RBRACKET,  // ]
    LBRACE,    // {
    RBRACE,    // }

    //operators
    ASSIGN,    // =
    PLUS,      // +
    MINUS,     // -
    BANG,      // !
    TILDE,     // ~

    // delimiters
    COMMA,     // ,
    DOT,       // .
    COLON,     // :
    SEMI,      // ;

    // comments
    LINECOMMENT,
    BLOCKCOMMENT,

    // end of the file
    EOF
}