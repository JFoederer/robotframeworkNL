def _fail_fail_pass_generator():
    yield False
    yield False
    yield True
gen = _fail_fail_pass_generator()

def pass_at_the_third_attempt():
    return next(gen)
