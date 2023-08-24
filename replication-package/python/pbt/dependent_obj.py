from json import JSONEncoder

class Dependent(JSONEncoder):
    
    def __init__(self, name, stars, pbt_file_path, url):
        self.__name = name
        self.__stars = stars
        self.__pbt_file_path = pbt_file_path
        self.__url = url

    def __str__ (self):
        return f'/******************************************************************/\n Repository name: {self.__name} ===> Stars: {self.__stars} ::: file that uses hypothesis: {self.__pbt_file_name}\n'

    def __repr__(self):
        return self.__str__()



class DependentEncoder(JSONEncoder):

    def default(self, object):

        if isinstance(object, Dependent):
            return object.__dict__

        else:
            return JSONEncoder.default(self, object)