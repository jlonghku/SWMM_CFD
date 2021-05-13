from importlib import import_module


class runModel(object):
    @classmethod
    def clsImport(cls,models):
        cls.models={}
        for i in models:
            cls.models[i]=import_module(i)