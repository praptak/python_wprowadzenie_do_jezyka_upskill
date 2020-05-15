import pytest

from lottery.participants import ParticipantWeighed, create_list_with_weighed_participants


@pytest.fixture()
def mock_list_dicts():
    participant_a = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5).__dict__
    participant_b = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 2).__dict__
    participant_c = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 4).__dict__
    participant_d = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 1).__dict__
    participant_e = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 1).__dict__
    participants_data = [
        participant_a,
        participant_b,
        participant_c,
        participant_d,
        participant_e
    ]

    for p in participants_data:
        p['id'] = p.pop('participant_id')

    return participants_data


def test_create_list_with_weighed_participants(mock_list_dicts):
    create_list_with_weighed_participants(mock_list_dicts)
