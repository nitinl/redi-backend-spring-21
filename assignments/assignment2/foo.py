"""
Date: 29/3/21
Description: 
"""

class Employee:
   def __init__(self, id, name, salary):
       self.id = id
       self.name = name
       self.salary = salary

   def calculate_payroll(self):
      return self.salary

class Contractor(Employee):
   def __init__(self, id, name, salary, hours):
       super(self).__init__(id, name, salary)
       self.hours = hours

   def calculate_payroll(self):
       return self.salary * self.hours


class A:
   def process(self):
       print('A process()')

class B(A):
    def process(self):
        print('B process()')

if __name__ == '__main__':
    obj = B()
    obj.process()