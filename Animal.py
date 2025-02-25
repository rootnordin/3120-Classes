class Animal:
    def __init__(self, name):
        self.__name = name 
        print("hello, I am", self.__name)

    def talk(self):
        print("hi")

class Animal:
    def __init__(self, name, species):
        self.__name = name
        self.__species = species
        print(f"Hello, I am {self.__name}, a {self.__species}")

    def talk(self):
        print("Hi")

    def eat(self, food):
        print(f"{self.__name} is eating {food}.")

    def sleep(self, hours):
        print(f"{self.__name} is sleeping for {hours} hours.")

    def walk(self, distance):
        print(f"{self.__name} walked {distance} kilometers.")

    def describe(self):
        print(f"My name is {self.__name} and I am a {self.__species}.")

    def set_name(self, new_name):
        self.__name = new_name
        print(f"My new name is {self.__name}.")

    def make_sound(self, sound):
        print(f"{self.__name} says {sound}!")

    def play(self, activity):
        print(f"{self.__name} is playing {activity}.")

    def age(self, years):
        print(f"{self.__name} is {years} years old.")

    def run(self, speed):
        print(f"{self.__name} is running at {speed} km/h.")

    def jump(self, height):
        print(f"{self.__name} jumped {height} meters high.")
    
