def match_eq(r, s):
    if r == "":
        return True
    if s == "":
        return r == "$"
    (r := r[1:]) and (esc := True) if r[0] == "\\" else (esc := False)  # coding golf
    if len(r) > 1:
        if r[1] == "?":
            return match_eq(r[2:], s) or match_eq(r[0] + r[2:], s)
        if r[1] == "*":
            return match_eq(r[2:], s) or match_eq(r, s[1:])
        if r[1] == "+":
            return match_eq(r[0] + r.replace("+", "*", 1), s)
    return match_eq(r[1:], s[1:]) if r[0] == s[0] or not esc and r[0] == "." else False


def match_uneq(r, s):
    return match_eq(r, s) or s != "" and match_uneq(r, s[1:])


def match(r, s):
    return match_eq(r[1:], s) if r.startswith("^") else match_uneq(r, s)


if __name__ == "__main__":
    print(match(*input().split("|")))
