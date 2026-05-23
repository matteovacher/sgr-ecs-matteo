


class Config : 
    def __init__(self, config) :
        for key, value in config.items() : 
            setattr(self, key, value)

        
    def __str__(self) :
        result = ""
        for key, value in self.__dict__.items() :
            result += "\t{} : {}\n".format(key, value)
        return result