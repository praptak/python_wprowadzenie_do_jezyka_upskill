from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Participant:
    id: int
    first_name: str
    last_name: str

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return self.full_name()

    def __gt__(self, other):
        return self.full_name() + str(self.id) > other.full_name() + str(other.id)

    def __le__(self, other):
        return self.full_name() + str(self.id) < other.full_name() + str(other.id)


@dataclass(frozen=True, eq=True)
class ParticipantWeighed(Participant):
    weight: int = 1

    def get_all_info(self):
        return f'{super().full_name()}, weight={self.weight}'
