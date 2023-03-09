import re


def valid_length(pwd, min_=8, max_=16):
    if min_ <= len(pwd) <= max_:
        return True, None
    else:
        return False, "密码长度应在8到16位"


def valid_number(pwd):
    match = re.search("[0-9]+", pwd)
    if match:
        return True, None
    else:
        return False, "密码应该包含数字"


def valid_upper(pwd):
    res = re.search("[A-Z]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该包含大写字母"


def valid_lower(pwd):
    res = re.search("[a-z]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该包含小写字母"


def valid_start(pwd):
    res = re.search("^[a-zA-Z0-9]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该以字母或数字开头"


def check_special(pwd):
    res = re.search(r"[~!@#$%^&*()\-_=+]+", pwd)
    if res:
        return True, None
    else:
        return False, "密码应该至少包含一个特殊字符"


def check_pwd(pwd):
    for temp in [valid_length, valid_number, valid_upper, valid_lower, valid_start, check_special]:
        is_ok, error = temp(pwd)
        if not is_ok:
            return False, error
    return True, None


# def check_password(pwd):
#     res = re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%^&*()_\-+])[A-Za-z\d~!@#$%^&*()_\-+]{8,16}$", pwd)
#     return True if res else False


if __name__ == '__main__':
    print("check_pwd:", check_pwd("ssFs#ss0sss"))
