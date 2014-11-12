__author__ = 'renatomoitinhodias'

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

schemas ={

    "example":{
        "columns":["uid","name"]
    }
}
