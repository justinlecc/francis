import datetime
import parsedatetime

c = parsedatetime.Calendar()

test_cases = [
    "today at five o'clock",
    "today at 5pm",
    "right now"
]

for case in test_cases:

    print(c.nlp(case))
    continue

    case_pt, parse_status = c.parse(case)
    case_dt = datetime.datetime(*case_pt[:6])
    print("---------------------------------")
    print("case: " + case)
    print("result: " + str(case_dt))
    print("status: " + str(parse_status))
    print("---------------------------------")