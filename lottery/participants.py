from dataclasses import dataclass


@dataclass(frozen=True, eq=True, repr=False, order=True)
class Participant:
    first_name: str
    last_name: str
    participant_id: int

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return self.full_name()


@dataclass(frozen=True, eq=True, repr=False, order=True)
class ParticipantWeighed(Participant):
    weight: int = 1
