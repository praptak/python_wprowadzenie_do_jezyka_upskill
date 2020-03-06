class Participant:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return self.get_fullname()

    # to check uniqueness of object
    def __hash__(self):
        return hash((self.id, self.first_name, self.last_name))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    # added to allow sorting list of objects by fullname
    def __gt__(self, other):
        return self.get_fullname() > other.get_fullname()

    def __le__(self, other):
        return self.get_fullname() < other.get_fullname()


class ParticipantWeighed(Participant):
    def __init__(self, id, first_name, last_name, weight=1, *args, **kwargs):
        super().__init__(id, first_name, last_name)
        self.weight = weight

    def __repr__(self):
        return self.get_all_info()

    def get_all_info(self):
        return f'{super().get_fullname()} ,weight={self.weight}'

    @classmethod
    def from_dict(cls, dict_source):
        return cls(**dict_source)
