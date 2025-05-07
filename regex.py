from abc import ABC, abstractmethod


class State(ABC):
    """
    base class for states in the FSM
    state can have multiple next states
    """
    def __init__(self):
        self.next_states = []

    @abstractmethod
    def check_self(self, char: str) -> bool:
        """
        function checks whether occured character is handled by current ctate
        """
        pass


class StartState(State):
    """
    state for start of the string
    """

    def check_self(self, char):
        return True


class TerminationState(State):
    """
    state for end of the string
    """

    def check_self(self, char):
        return True


class DotState(State):
    """
    state for . character (any character accepted)
    """

    def check_self(self, char: str):
        return True


class AsciiState(State):
    """
    state for alphabet letters or numbers
    """

    def __init__(self, symbol: str):
        super().__init__()
        self.symbol = symbol

    def check_self(self, char: str):
        return char == self.symbol


class StarState(State):
    """
    state for * character (0 or more times)
    """

    def __init__(self, checking_state):
        super().__init__()
        self.next_states.append(self)
        self.checking_state = checking_state

    def check_self(self, char):
        return self.checking_state.check_self(char)



class PlusState(State):
    """
    state for + character (1 or more times)
    """

    def __init__(self, checking_state):
        super().__init__()
        self.next_states.append(self)
        self.checking_state = checking_state

    def check_self(self, char):
        return self.checking_state.check_self(char)


class CharClassState(State):
    """
    state for character classes like [a-z0-9]
    """

    def __init__(self, allowed_chars: set[str]):
        super().__init__()
        self.allowed_chars = allowed_chars

    def check_self(self, char: str):
        return char in self.allowed_chars


class RegexFSM:
    def __init__(self, pattern: str):
        self.start_state = StartState()
        current_state = self.start_state
        i = 0

        while i < len(pattern):
            char = pattern[i]

            if char == "[":
                end_idx = pattern.find("]", i)
                if end_idx == -1:
                    raise ValueError("Unclosed character class '['")

                class_expr = pattern[i + 1:end_idx]
                allowed_chars = set()

                j = 0
                while j < len(class_expr):
                    if j + 2 < len(class_expr) and class_expr[j + 1] == "-":
                        start, end = class_expr[j], class_expr[j + 2]
                        allowed_chars.update(chr(c) for c in range(ord(start), ord(end) + 1))
                        j += 3
                    else:
                        allowed_chars.add(class_expr[j])
                        j += 1

                new_state = CharClassState(allowed_chars)
                i = end_idx
            else:
                if char == ".":
                    new_state = DotState()
                elif char.isascii():
                    new_state = AsciiState(char)
                elif char in ["*", "+"]:
                    raise ValueError("'*' або '+' не можуть бути на початку шаблону")
                else:
                    raise ValueError(f"Недопустимий символ: {char}")

            if i + 1 < len(pattern):
                next_char = pattern[i + 1]
                if next_char == "*":
                    new_state = StarState(new_state)
                    i += 1
                elif next_char == "+":
                    new_state = PlusState(new_state)
                    i += 1

            current_state.next_states.append(new_state)
            current_state = new_state
            i += 1

        current_state.next_states.append(TerminationState())


    def check_string(self, string):
        """
        checks if the string matches the regex pattern
        """

        def dfs(state, i):
            for next_state in state.next_states:
                if isinstance(next_state, StarState) and next_state != state:
                    if dfs(next_state, i):
                        return True

                if i < len(string) and next_state.check_self(string[i]):
                    if dfs(next_state, i + 1):
                        return True

                if i >= len(string) and isinstance(next_state, TerminationState):
                    return True
            return False

        return dfs(self.start_state, 0)
