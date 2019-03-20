grammar TableGen;

options
{
    language = Python3;
}

expression : (ws | statementExpression)* EOF ;

statementExpression : switchDefinition ;

switchDefinition :
        'def' (ws definitionName)? ws?
        ':'
        diagnosticProperties
        ';' ;

diagnosticProperties :
        ws? classDefinition ws? (',' ws? classDefinition ws?)*
    ;

definitionName : switchClass ;

classDefinition :
        classDefinitionName ws?
        '<' ws? switchName ws?
        (',' ws? identifierList)?
         ws? '>' ;

classDefinitionName : classname ;

switchName : emptySwitchName | ('"' switchText '"') ;

emptySwitchName : '""' ;

switchClass : classname ;

identifierList :
        '['
        ws? identifierReference ws?
        (',' ws? identifierReference ws?)*
        ']' ;

identifierReference :
        referencedName
// TODO clang 3.1 uses this syntax inside identifier lists.
//    | classDefinition
    ;

referencedName :
        switchClass
    ;

classname : IDENTIFIERTEXT ;

ws : (COMMENT | WHITESPACE)+ ;

IDENTIFIERTEXT : ('a'..'z' | 'A'..'Z' | '0'..'9')+;

WHITESPACE : (' '|'\t'|'\n')+;

START_COMMENT : '//' ;
COMMENT_CHARS : ~[\r\n] ;
END_COMMENT : '\n' ;

COMMENT : START_COMMENT COMMENT_CHARS* END_COMMENT ;

WHITESPACE_COMMENT : (WHITESPACE)+ ;

switchText : (~'"')+ ;
