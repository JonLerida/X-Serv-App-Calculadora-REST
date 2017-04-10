#!/usr/bin/python3

#
# Simple calculator: add, subs, mult, div
# Can only perform one operation "at a time"
# (well, one of each of the operations"
#
# Copyright Jesus M. Gonzalez-Barahona 2009
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# October 2009
#


"""
X-Serv-App-Calculadora-REST

Ejercicio de asignaturas de aplicaciones web. Servicios que interoperan.
Calculadora simple versión REST.
Enunciado

Realizar una calculadora de las cuatro operaciones aritméticas básicas
(suma, resta, multiplicación y división), siguiendo los principios REST,
a la manera del sumador simple versión REST.
"""

import webappmulti
import urllib.parse

def decorateHTML (text):

    return ("<html><body>" + text + "</body></html>")

class operation (webappmulti.app):
    """Void class for all operations (sum, sub, mul, div)
    Acts when receiving the following HTTP requests:
     - PUT (arguments in body, as query string): performs the operation
         (and returns the result of the operation)
     - GET: returns the result of the operation
    Methods operate and sign should be overidden by children classes
    """

    def operate (self, oper1, oper2):
        """Placeholder operation, to be extended by children of this class.
        Returns the value of applying it to oper1, oper2."""

        return None

    def sign (self):
        """Placeholder operation, to be extended by children of this class.
        Returns the sign of the operation."""

        return None

    def parse (self, request, rest):
        verb = request.split(' ',1)[0]
        parts = request.split('\r\n\r\n',1)
        if len (parts) == 2:
            body = parts[1]
        else:
            body = ""

        return (verb, body)

    def process (self, verb, body):
        #aquí verb= tupla.

        """
        como estoy heredando los métodos de la clase padre, los argumentos que recibe esta funcion no encajan bien con los que
        tiene la clase padre (webAppmulti), de forma que lo que debería ser 'verb' y 'body' no lo son exactamente.
            verb[0] --> get, post...
            verb[1]--> cuerpo de la petición
            body --> lo que va después de /add/[...]
        """

        body = verb[1]
        verb = verb[0]
        rest = body
        print('Método: '+verb)
        print('Cuerpo: '+body)
        if verb == 'PUT':
            params = urllib.parse.parse_qs(body)
            try:
                self.oper1 = int(params['oper1'][0])
                self.oper2 = int(params['oper2'][0])
                self.result = self.operate (self.oper1, self.oper2)
                success = True
            except:
                success = False
                (error, message) = ("400 Error",
                                    "Error in parameters for operation")
        elif verb == 'GET':
            success = True
        else:
            success = False
            (error, message) = ("400 Error",
                                "HTTP verb " + verb + " not supported")

        if success:
            return ("200 OK", decorateHTML(str(self.oper1) + self.sign() +
                                           str(self.oper2) +
                                           "=" + str(self.result)))
        else:
            return (error, decorateHTML(message))

    def __init__ (self):
        """
        esto se ejecuta cada vez que iniciemos una clase"""
        self.oper1 = 0
        self.oper2 = 0
        self.result = 0

class add (operation):
    def operate (self, oper1, oper2):

        return oper1 + oper2

    def sign (self):

        return '+'

class sub (operation):
    def operate (self, oper1, oper2):

        return oper1 - oper2

    def sign (self):

        return '-'

class mul (operation):
    def operate (self, oper1, oper2):

        return oper1 * oper2

    def sign (self):

        return '*'

class div (operation):
    def operate (self, oper1, oper2):

        return oper1 / oper2

    def sign (self):

        return '/'

if __name__ == "__main__":
    addObj = add()
    subObj = sub()
    mulObj = mul()
    divObj = div()
    #si ejecuto esto, se crea una clase de cada tipo, y la clase multi. que es llamada desde webappmulti
    multiCalc = webappmulti.webApp ("localhost", 1234,
                                    {'/add': addObj,
                                     '/sub': subObj,
                                     '/mul': mulObj,
                                     '/div': divObj,})
