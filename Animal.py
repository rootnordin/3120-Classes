class Animal:
    def __init__(self, name):
        self._name = name 
        print("Hello, I am", self._name)

    def talk(self):
        print("Hi")

    def walk(self):
        print(f"{self.__name} is walking.")

    def eat(self, food):
        print(f"{self.__name} is eating {food}.")