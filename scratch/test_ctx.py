from contextlib import contextmanager

@contextmanager
def _conn():
    print("start")
    try:
        yield "con"
        print("commit")
    except Exception:
        print("rollback")
    finally:
        print("close")

def test():
    with _conn() as con:
        print("inside")
        # no return

test()
