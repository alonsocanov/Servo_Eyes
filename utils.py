def regression(offset, max_duty, min_duty, liberty):
    print(liberty)
    difference = max_duty - min_duty
    print(difference)
    m = difference / liberty
    print(m)
    duty_cycle = (offset * m) + min_duty
    print(duty_cycle)
    return int(duty_cycle)