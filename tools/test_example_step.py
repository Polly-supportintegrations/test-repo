"""What example_step promises, checked. Run every test with `python3 tools/run_tests.py`."""

from example_step import example_step


def check(label, got, want):
    assert got == want, f"{label}: wanted {want}, got {got}"
    print(f"  ok  {label}")


def run():
    check("a phrase that is there is found",
          example_step("Please disregard this", ["disregard"]),
          {"found": [{"phrase": "disregard", "at": 7}], "count": 1})
    check("matching ignores case",
          example_step("PLEASE DISREGARD", ["disregard"])["count"], 1)
    check("a phrase that is absent is not invented",
          example_step("nothing to see", ["disregard"]), {"found": [], "count": 0})
    check("no phrases means nothing found", example_step("anything", [])["count"], 0)


if __name__ == "__main__":
    run()
