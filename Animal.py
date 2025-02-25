class Animal:
    def __init__(self, name):
        self.__name = name 
        print("hello, I am", self.__name)

    def talk(self):
        print("hi")

def set_name9(self, new_name):
    " Change the name of the animal"
    self.__name == new_name
    print("My new name is", self.__name)

def get_name(self):
    " Return the name of the animal"
    return self.__name
