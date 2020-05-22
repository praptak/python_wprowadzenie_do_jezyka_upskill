import pytest

from lottery.participants import ParticipantWeighed, create_list_with_weighed_participants


@pytest.fixture()
def mock_input_data_example():
    return [
        {'first_name': 'FirstName_a', 'last_name': 'Lastname_a', 'weight': 5, 'id': 1},
        {'first_name': 'FirstName_a', 'last_name': 'Lastname_a', 'weight': 2, 'id': 1},
        {'first_name': 'FirstName_a', 'last_name': 'Lastname_a', 'weight': 4, 'id': 1},
        {'first_name': 'FirstName_a', 'last_name': 'Lastname_a', 'weight': 1, 'id': 1},
        {'first_name': 'FirstName_a', 'last_name': 'Lastname_a', 'weight': 1, 'id': 1}
    ]


@pytest.fixture()
def mock_expected_result_from_example():
    participant_a = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 5)
    participant_b = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 2)
    participant_c = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 4)
    participant_d = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 1)
    participant_e = ParticipantWeighed('FirstName_a', 'Lastname_a', 1, 1)
    return [
        participant_a,
        participant_b,
        participant_c,
        participant_d,
        participant_e
    ]


@pytest.fixture()
def mock_input_data_empty_example():
    return []


@pytest.fixture()
def mock_expected_result_from_empty_example():
    return []


@pytest.fixture(params=
[
    ('mock_input_data_empty_example', 'mock_expected_result_from_empty_example'),
    ('mock_input_data_example', 'mock_expected_result_from_example')
]
)
def data_fixtures(request):
    return (
        request.getfixturevalue(request.param[0]),
        request.getfixturevalue(request.param[1])
    )


def test_create_list_with_weighed_participants(data_fixtures):
    input_data = data_fixtures[0]
    expected_output_data = data_fixtures[1]
    actual_output_data = create_list_with_weighed_participants(input_data)
    assert expected_output_data == actual_output_data
