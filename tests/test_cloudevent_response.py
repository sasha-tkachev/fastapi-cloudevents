from fastapi_cloudevents.cloudevent_response import _encoded_string


def test_bytes_is_already_encoded():
    v = b"Hello World"
    assert _encoded_string(v) is v


def test_str_should_be_encoded_in_utf_8():
    assert _encoded_string("Hello World") == b"Hello World"
