from maico.model.interface import MaicoModel


class FirstActionModel(MaicoModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def predict(self, target):
        return 1
