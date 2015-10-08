#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 
# version 1.0 - programmes 'lexico-grammatical' de parser d'arguments
# >> aide substantielle de Ludovic
# 
# Copyright (c) 2015 Jonathan Viandier <jonathan.viandier@free.fr>
#       Tuteur de stage        : Sylvain Antoine <santoine@univ-jfc.fr>
#       Administrateur Système : Ludovic Pouzenc <lpouzenc@univ-jfc.fr>
#
# Ce programme a été écrit par Jonathan Viandier pour une éventuelle 
# amélioration du système de clonage des machines clientes,
# au sein de l'Université Jean-Francois Champollion.

import os, readline
import ply.lex as lex
import ply.yacc as yacc


class Parser:
    """
    Base class for a lexer/parser that has the rules defined as methods
    """
    tokens = ()
    precedence = ()

    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.names = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"
        #print self.debugfile, self.tabmodule

        # Build the lexer and parser
        lex.lex(module=self, debug=self.debug)
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    

class IPRange(Parser):

    tokens = (
        'NUMBER', 'DOT', 'MINUS','COMA', 'LEFT_CURLY_BRACKET','RIGHT_CURLY_BRACKET'
        )

    # Tokens
    t_DOT    = r'\.'
    t_MINUS   = r'-'
    t_COMA     = r','
    t_LEFT_CURLY_BRACKET   = r'{'
    t_RIGHT_CURLY_BRACKET  = r'}'

    list_ip = []
    
    def run(self, s):
        yacc.parse(s)
        return self.list_ip

    def t_NUMBER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
#            print "Integer value too large", t.value
            t.value = 0
#        print "parsed number %s" % repr(t.value)
        return t

    t_ignore = " \t"

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")
    
    def t_error(self, t):
#        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    # Parsing rules
    precedence = ( )

    def p_iprange(self, p):
        'iprange : expr DOT expr DOT expr DOT expr'
        for e1 in p[1]:
            for e2 in p[3]:
                for e3 in p[5]:
                    for e4 in p[7]:
                        self.list_ip.append("%d.%d.%d.%d"%(e1,e2,e3,e4))
                        

#    def p_iprange(self, p):
#        'iprange : NUMBER DOT NUMBER DOT NUMBER DOT expr'
#        for e in p[7]:
#            print "-> %d.%d.%d.%d"%(p[1],p[3],p[5],e)

    def p_expr_number(self, p):
        'expr : NUMBER'
        p[0] = [ p[1] ]

    def p_expr_rangelist(self, p):
        'expr : LEFT_CURLY_BRACKET rangelist RIGHT_CURLY_BRACKET'
        p[0] = p[2]

    def p_rangelist_single(self, p):
        'rangelist : range'
        p[0] = p[1]
    
    def p_rangelist_multiple(self, p):
        'rangelist : range COMA rangelist'
        p[0] = p[1] + p[3]

    def p_range_single(self, p):
        'range : NUMBER'
        p[0] = [ p[1] ]

    def p_range_multiple(self, p):
        'range : NUMBER MINUS NUMBER'
        p[0] = range(p[1], p[3]+1)

    def p_error(self, p):
        print "Syntax error at '%s'" % p.value

