# Regex FSM Lab

This project implements a Finite State Machine (FSM) for processing simplified regular expressions as part of a discrete mathematics course lab assignment.

## Goal

The goal is to parse a regular expression pattern and construct a deterministic state machine that can match input strings according to that pattern.

## Features

Supported elements of regular expressions:
- `a`, `b`, ... : exact character match
- `.` : any single character
- `*` : zero or more repetitions of the previous element
- `+` : one or more repetitions of the previous element
- `[a-z0-9]` : character classes with optional ranges

## Architecture

### State Classes

Each regex construct is represented as a subclass of an abstract `State` class:
- `AsciiState`: matches a specific character.
- `DotState`: matches any single character.
- `StarState`: matches zero or more repetitions.
- `PlusState`: matches one or more repetitions.
- `CharClassState`: matches a character from a set or range.
- `StartState` and `TerminationState`: define the start and end of matching.

### RegexFSM

The `RegexFSM` class is responsible for:
- Parsing the regex pattern.
- Building a graph of `State` objects connected by transitions.
- Performing depth-first search (DFS) through possible state transitions when checking a string.

## Usage

Example code:
```python
fsm = RegexFSM("a[0-9]+b")
print(fsm.check_string("a1b"))       # True
print(fsm.check_string("a99b"))      # True
print(fsm.check_string("ab"))        # False
