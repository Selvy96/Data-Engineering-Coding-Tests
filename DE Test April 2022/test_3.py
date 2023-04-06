# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.


# [TODO]: fix the function
def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""
    list_of_nums = time_str.split(":")
    answer = 0
    for num in list_of_nums:
        answer += int(num)
    return answer


def test_sum_current_time_returns_int():
    """Tests sum current time returns a number"""
    result = sum_current_time("04:05:33")

    assert isinstance(result, int)

def test_sum_current_time_returns_correct_answer():
    """Tests sum current time function returns correct answer"""
    result = sum_current_time("03:04:25")
    assert result == 32