#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: dbc
"""

import re

class Variables(object):
    '''Container for variables
    
    Class that packages the access to/storage of variables
    '''
    def __init__(self, source = "Unknown", variables = None):
        self.variables = {}
        self.source = source
        if variables is not None:
            self.update(variables)
        
    def update(self, other):
        self.variables.update(other.variables)
    
    def set_var(self, variable):
        if re.match('^\s*[_a-zA-Z0-9][-_a-zA-Z0-9]*\s*=', variable) is None:
            raise Exception("Unparsable variable '%s' from %s" % (variable, self.source))
        (k, v) =  [ x.strip() for x in variable.split("=", 1) ]
        if k in self.variables:
            raise Exception("variable %s is set twice from: %s" % (k, self.source))
        self.variables[k] =  v

    def read_variables(self, filename):
        variables = Variables(filename);
        with open(filename) as stream:
            for line in stream:
                if re.match('^\s*(?:#.*)?$', line) is not None:
                    continue
                variables.set_var(line)
        self.update(variables)

    def env(self):
        return self.variables


class Characters(object):
    '''
    '''
    def __init__(self, var):
        self.chars = list(var).__iter__()
    def get(self):
        try:
            return self.chars.__next__()
        except StopIteration as e:
            return None

convertors = {
        'lower': lambda s: s.lower(),
        'upper': lambda s: s.upper(),
        'bool': lambda s: s.lower() in [ '1', 'yes', 'true' ],
        'int': lambda s:  int(s)
}

class Substituter(object):
    '''
    '''
    def __init__(self, variables = None):
        self.env = {}
        if variables is not None:
            self.env = variables

    def with_env(self, env):
        all_env = self.env.copy()
        all_env.update(env)
        return Substituter(all_env)
        
    def expand(self, var):
        expanded = []
        chars = Characters(var)
        c = chars.get()
        convert = lambda s: s
        while c is not None:
            if c is '\\':
                c = chars.get()
                if c is None:
                    raise Exception("Dangling \\ in: %s" % var)
                expanded.append(c)
                c = chars.get()
            elif c is '$':
                c = chars.get()
                env = []
                if c is '{':
                    while True:
                        c = chars.get()
                        if c is '}':
                            break
                        elif c.isalnum() or c in "_-":
                            env.append(c)
                        elif c is None:
                            raise Exception("Unclosed ${ in: %s" % var)
                        elif c is ':':
                            convert = self.read_convertor(chars, var)
                            break
                        else:
                            raise Exception("Invalid character in ${: %s" % c)
                    c = chars.get()
                elif c.isalnum() or c in "_":
                    env.append(c)
                    while c is not None:
                        c = chars.get()
                        if c is not None and ( c.isalnum() or c in "_"):
                            env.append(c)
                        else:
                            break
                else:
                    raise Exception("Unexpected character after $ in: %s" % var)
                env = ''.join(env)
                if env not in self.env:
                    raise Exception("Use of undefined variable %s in: %s" % (env, var))
                expanded.append(self.env[env])
            else:
                expanded.append(c)
                c = chars.get()
        s = ''.join(expanded)
        return convert(s);

    def read_convertor(self, chars, var):
        c = chars.get()
        s = ''
        while c is not None:
            if c is '}':
                if s not in convertors:
                    raise Exception("unknown convertor: :%s in %s" %(s, var))
                return convertors[s]
            s = s + c
            c = chars.get()
        raise Exception("Unclosed ${ in: %s" % var)

    def traverse(self, obj):
        if isinstance(obj, dict):
            for k,v in obj.items():
                obj[k] = self.traverse(v)
        elif isinstance(obj, list):
            obj = [ self.traverse(v) for v in obj ]
        elif isinstance(obj, str):
            obj = self.expand(obj)
        return obj

        
