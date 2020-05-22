from abc import ABC, abstractmethod


class Department:
    '''
    Esta classe é uma representação de departamentos de uma organização.

    Attributes:
        name(string): Representa o nome do departamento.
        code(int): Representa o código identificador único do departamento.
    '''

    def __init__(self, name, code):
        self.__name = name
        self.__code = code

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code


class Employee(ABC):
    '''
    Esta é uma classe abstrata que define a representação de genérica de um
    empregado.

    Attributes:
        code(int): Representa o código identificador único do empregado.
        name(string): Representa o nome do empregado.
        salary(float): Representa o salário do empregado.
        hours(int): Representa o número de horas de período de trabalho.
    '''

    def __init__(self, code, name, salary):
        self.__code = code
        self.__name = name
        self.__salary = salary
        self.__hours = 8

    @abstractmethod
    def calc_bonus(self):
        pass

    @abstractmethod
    def get_hours(self):
        pass

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, code):
        self.__code = code

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, salary):
        self.__salary = salary

    def get_hours(self):
        return self.__hours


class Manager(Employee):
    '''
    Esta é uma classe que define a representação de um empregado com o cargo
    de gerente na organização.

    Attributes:
        code(int): Representa o código identificador único do empregado.
        name(string): Representa o nome do empregado.
        salary(float): Representa o salário do empregado.
        hours(int): Representa o número de horas de período de trabalho.
    '''

    def __init__(self, code, name, salary):
        super().__init__(code, name, salary)
        self.__department = Department('managers', 1)

    def calc_bonus(self):
        '''Calcula e retorna o valor do bônus que será recebido.'''
        return self.salary * 0.15

    def get_department(self):
        return self.__department.name

    def set_departament(self, department):
        self.__department.name = department


class Seller(Employee):
    '''
    Esta é uma classe que define a representação de um empregado com o cargo
    de gerente na organização.

    Attributes:
        code(int): Representa o código identificador único do empregado.
        name(string): Representa o nome do empregado.
        salary(float): Representa o salário do empregado.
        hours(int): Representa o número de horas de período de trabalho.
    '''

    def __init__(self, code, name, salary):
        super().__init__(code, name, salary)
        self.__department = Department('sellers', 2)
        self.__sales = 0

    def get_sales(self):
        '''Retorna o valor total das vendas realizadas.'''
        return self.__sales

    def put_sales(self, sales):
        '''Adiciona o valor de novas vendas ao total.'''
        self.__sales += sales

    def get_department(self):
        return self.__department.name

    def set_departament(self, name):
        self.__department.name = name

    def calc_bonus(self):
        '''Calcula e retorna o valor do bônus que será recebido.'''
        return self.get_sales() * 0.15
