import pytest


def test_root_path(client_function):
    response = client_function.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": 2}


def test_app_companies_10(client_function, company_factory_function):
    expected = 10
    company_factory_function.create_batch(expected)
    response = client_function.get("/companies")
    assert response.status_code == 200
    assert response.json() == {"count": expected}


def test_app_companies_3(client_function, company_factory_function):
    expected = 3
    company_factory_function.create_batch(expected)
    response = client_function.get("/companies")
    assert response.status_code == 200
    assert response.json() == {"count": expected}


def test_app_companies_session(client_session, company_factory_session):
    expected = 3
    company_factory_session.create_batch(expected)
    response = client_session.get("/companies")
    assert response.status_code == 200
    assert response.json() == {"count": expected}


@pytest.mark.xfail(reason="there are existing companies left in the database")
def test_app_companies_session_fail(client_session, company_factory_session):
    expected = 3
    company_factory_session.create_batch(expected)
    response = client_session.get("/companies")
    assert response.status_code == 200
    assert response.json() == {"count": expected}
