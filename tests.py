from regex import RegexFSM

regex_pattern = "a*4.+hi"
regex_compiled = RegexFSM(regex_pattern)

assert regex_compiled.check_string("aaaaaa4uhi") == True
assert regex_compiled.check_string("4uhi") == True
assert regex_compiled.check_string("meow") == False


regex_pattern = "a"
regex_compiled = RegexFSM(regex_pattern)

assert regex_compiled.check_string("a") == True
assert regex_compiled.check_string("b") == False
assert regex_compiled.check_string("baa") == False


regex_pattern = "a*b"
regex_compiled = RegexFSM(regex_pattern)

assert regex_compiled.check_string("aaab") == True
assert regex_compiled.check_string("b") == True
assert regex_compiled.check_string("aaac") == False
assert regex_compiled.check_string("a") == False


regex_pattern = "a*b.c+d"
regex_compiled = RegexFSM(regex_pattern)

assert regex_compiled.check_string("aaabxcd") == True
assert regex_compiled.check_string("aaabxccd") == True
assert regex_compiled.check_string("aaabd") == False


regex_pattern = "a*a*a*"
regex_compiled = RegexFSM(regex_pattern)

assert regex_compiled.check_string("aaaa") == True
assert regex_compiled.check_string("bbbbb") == False


regex_pattern = "a+b+c+"
regex_compiled = RegexFSM(regex_pattern)

assert regex_compiled.check_string("aaabbbccc") == True
assert regex_compiled.check_string("aaacc") == False

fsm = RegexFSM("[a-c]+1")
assert fsm.check_string("abcabc1") == True
assert fsm.check_string("abcd1") == False

print("All tests passed.")
