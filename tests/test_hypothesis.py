from hypothesis import given, settings
from hypothesis.strategies import text, characters


@given(text(characters(max_codepoint=1000, blacklist_categories=("Cc", "Cs"))))
@settings(max_examples=5000)
def test_root_path(client_session, text):
    response = client_session.post(f"/companies", json={"name": text})
    assert response.status_code == 200
