#!/usr/bin/env python
# $Id:  $
# Author:
# Copyright: This module has been placed in the public domain.

"""
A finite state machine specialized for regular-expression-based text filters,
this module defines the following classes:

- `StateMachine`, a state machine
- `State`, a state superclass
- `StateMachineWS`, a whitespace-sensitive version of `StateMachine`
- `StateWS`, a state superclass for use with `StateMachineWS`
- `SearchStateMachine`, uses `re.search()` instead of `re.match()`
- `SearchStateMachineWS`, uses `re.search()` instead of `re.match()`
- `ViewList`, extends standard Python lists.
- `StringList`, string-specific ViewList.

Exception classes:

- `StateMachineError`
- `UnknownStateError`
- `DuplicateStateError`
- `UnknownTransitionError`
- `DuplicateTransitionError`
- `TransitionPatternNotFound`
- `TransitionMethodNotFound`
- `UnexpectedIndentationError`
- `TransitionCorrection`: Raised to switch to another transition.
- `StateCorrection`: Raised to switch to another state & transition.

Functions:

- `string2lines()`: split a multi-line string into a list of one-line strings


How To Use This Module
======================
(See the individual classes, methods, and attributes for details.)

1. Import it: ``import statemachine`` or ``from statemachine import ...``.
   You will also need to ``import re``.

2. Derive a subclass of `State` (or `StateWS`) for each state in your state
   machine::

       class MyState(statemachine.State):

   Within the state's class definition:

   a) Include a pattern for each transition, in `State.patterns`::

          patterns = {'atransition': r'pattern', ...}

   b) Include a list of initial transitions to be set up automatically, in
      `State.initial_transitions`::

          initial_transitions = ['atransition', ...]

   c) Define a method for each transition, with the same name as the
      transition pattern::

          def atransition(self, match, context, next_state):
              # do something
              result = [...]  # a list
              return context, next_state, result
              # context, next_state may be altered

      Transition methods may raise an `EOFError` to cut processing short.

   d) You may wish to override the `State.bof()` and/or `State.eof()` implicit
      transition methods, which handle the beginning- and end-of-file.

   e) In order to handle nested processing, you may wish to override the
      attributes `State.nested_sm` and/or `State.nested_sm_kwargs`.

      If you are using `StateWS` as a base class, in order to handle nested
      indented blocks, you may wish to:

      - override the attributes `StateWS.indent_sm`,
        `StateWS.indent_sm_kwargs`, `StateWS.known_indent_sm`, and/or
        `StateWS.known_indent_sm_kwargs`;
      - override the `StateWS.blank()` method; and/or
      - override or extend the `StateWS.indent()`, `StateWS.known_indent()`,
        and/or `StateWS.firstknown_indent()` methods.

3. Create a state machine object::

       sm = StateMachine(state_classes=[MyState, ...],
                         initial_state='MyState')

4. Obtain the input text, which needs to be converted into a tab-free list of
   one-line strings. For example, to read text from a file called
   'inputfile'::

       input_string = open('inputfile').read()
       input_lines = statemachine.string2lines(input_string)

5. Run the state machine on the input text and collect the results, a list::

       results = sm.run(input_lines)

6. Remove any lingering circular references::

       sm.unlink()
"""

__docformat__ = 'restructuredtext'
# encoding: utf-8
import sys
import os

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(LOCAL_DIR)
sys.path.append(PROJECT_DIR)
sys.path.insert(0, '.')

"""
run with

    python bin/main.py 2>/dev/null

to push GObject warnings to /dev/null on linux
"""

if "-t" in sys.argv:
    os.environ['CADNANO_IGNORE_ENV_VARS_EXCEPT_FOR_ME'] = 'YES'


def main(args):
    """The main function (entry-point) in animDNA"""
    print(args)
    from cadnano import initAppWithGui
    app = initAppWithGui(args)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(sys.argv)
