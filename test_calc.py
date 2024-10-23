from calc.calculations import sum_calculation, tricky_divide


def test_sum():
    assert sum_calculation(2, 3) == 5


# @pytest.mark.skipif(reason="known defect")
def test_tricky_divide():
    expected_result = 2
    actual_result = tricky_divide(12, 6) == expected_result
    assert actual_result == expected_result, \
        f"Divide results failed. Expected {expected_result} but got {actual_result}"
