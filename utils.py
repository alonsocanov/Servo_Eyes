def regression(offset, min_duty, max_duty, liberty):
    difference = max_duty - min_duty
    m = difference / liberty
    duty_cycle = (offset * m) + min_duty
    return int(duty_cycle)