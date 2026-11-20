import pytest
from financial import get_response, get_soup, get_ans

def test_total_revenue_value():
    response = get_response('MSFT')
    row_title = get_soup('Total Revenue', response)
    ans = get_ans(row_title, 'Total Revenue')
    
    assert ans[0] == 'Total Revenue'

def test_return_type_is_tuple():
    response = get_response('MSFT')
    row_title = get_soup('Total Revenue', response)
    ans = get_ans(row_title, 'Total Revenue')
    
    assert type(ans) == tuple


def test_invalid_ticker():
    response = get_response('ZZZZZZZZZ')
    with pytest.raises(ValueError):
        get_soup('Total Revenue', response)

def test_response_status_code():
    response = get_response('MSFT')
    assert response.status_code == 200


def test_get_soup_returns_row_title():
    response = get_response('MSFT')
    row_title = get_soup('Total Revenue', response)
    assert row_title is not None


def test_invalid_field_raises_error():
    response = get_response('MSFT')
    with pytest.raises(ValueError):
        get_soup('Not A Real Field', response)


def test_ans_has_five_values():
    response = get_response('MSFT')
    row_title = get_soup('Total Revenue', response)
    ans = get_ans(row_title, 'Total Revenue')

    assert len(ans) == 6