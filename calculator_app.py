"""Streamlit calculator.

How to run (step by step, in PowerShell):

  Step 1. Open PowerShell and go to the project folder:
            cd C:\\Users\\pugaz\\source\\repos\\StreamlitProject

  Step 2. Install Streamlit (only needed once):
            python -m pip install streamlit

  Step 3. Start the app:
            python -m streamlit run calculator_app.py

          Use "python -m" because Windows blocks the streamlit.exe launcher.

  Step 4. Open the link shown in the terminal in your browser:
            http://localhost:8501
          (If it asks for an email, just press Enter to skip.)

  Step 5. To stop the app, click the terminal and press Ctrl+C.
"""

import math

import streamlit as st

st.set_page_config(page_title="Calculator", page_icon=":material/calculate:", layout="centered")

OPS = {
    "+": lambda a, b: a + b,
    "−": lambda a, b: a - b,
    "×": lambda a, b: a * b,
    "÷": lambda a, b: a / b,
    "^": lambda a, b: a**b,
    "mod": lambda a, b: a % b,
}

def factorial(x: float) -> int:
    if x != int(x) or x < 0:
        raise ValueError("Factorial needs a whole number, 0 or more")
    if x > 170:
        raise OverflowError
    return math.factorial(int(x))


def tangent(x: float) -> float:
    if x % 180 == 90:
        raise ValueError("Tangent is undefined here")
    return round(math.tan(math.radians(x)), 12) + 0.0


DOMAIN_ERRORS = {
    "√": "Square root needs a number of 0 or more",
    "log": "Log needs a number greater than 0",
    "ln": "Ln needs a number greater than 0",
}

# One-number functions applied to the value on the display (trig uses degrees).
FUNCS = {
    "√": math.sqrt,
    "x²": lambda x: x * x,
    "1/x": lambda x: 1 / x,
    "n!": factorial,
    "log": math.log10,
    "ln": math.log,
    "sin": lambda x: round(math.sin(math.radians(x)), 12) + 0.0,
    "cos": lambda x: round(math.cos(math.radians(x)), 12) + 0.0,
    "tan": tangent,
}


def fmt(value: float) -> str:
    """Format a number without trailing zeros (e.g. 2.0 -> '2')."""
    return f"{value:.10g}"


def init_state():
    st.session_state.setdefault("display", "0")
    st.session_state.setdefault("left", None)  # stored first operand
    st.session_state.setdefault("op", None)  # pending operator
    st.session_state.setdefault("fresh", True)  # next digit starts a new number
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("error", None)


def clear_all():
    st.session_state.display = "0"
    st.session_state.left = None
    st.session_state.op = None
    st.session_state.fresh = True
    st.session_state.error = None


def fail(message: str):
    clear_all()
    st.session_state.error = message


def press_func(name: str):
    s = st.session_state
    s.error = None
    x = float(s.display)
    try:
        result = FUNCS[name](x)
    except ZeroDivisionError:
        fail("Cannot divide by zero")
        return
    except OverflowError:
        fail("Result is too large")
        return
    except ValueError as e:
        fail(DOMAIN_ERRORS.get(name, str(e)))
        return
    s.history = ([f"{name}({fmt(x)}) = {fmt(result)}"] + s.history)[:10]
    s.display = fmt(result)
    s.fresh = True


def press_digit(digit: str):
    s = st.session_state
    s.error = None
    if s.fresh or s.display == "0":
        s.display = digit
    else:
        s.display += digit
    s.fresh = False


def press_dot():
    s = st.session_state
    s.error = None
    if s.fresh:
        s.display = "0."
        s.fresh = False
    elif "." not in s.display:
        s.display += "."


def press_pi():
    s = st.session_state
    s.error = None
    s.display = fmt(math.pi)
    s.fresh = True


def press_backspace():
    s = st.session_state
    if s.fresh:
        return
    s.display = s.display[:-1] or "0"
    if s.display == "-":
        s.display = "0"


def press_negate():
    s = st.session_state
    if s.display != "0":
        s.display = s.display[1:] if s.display.startswith("-") else "-" + s.display


def press_percent():
    s = st.session_state
    s.display = fmt(float(s.display) / 100)
    s.fresh = True


def evaluate() -> bool:
    """Apply the pending operation. Returns False on error."""
    s = st.session_state
    if s.op is None or s.left is None:
        return True
    right = float(s.display)
    try:
        result = OPS[s.op](s.left, right)
        if isinstance(result, complex):
            raise ValueError("Result is not a real number")
    except ZeroDivisionError:
        fail("Cannot divide by zero")
        return False
    except OverflowError:
        fail("Result is too large")
        return False
    except ValueError as e:
        fail(str(e))
        return False
    s.history = ([f"{fmt(s.left)} {s.op} {fmt(right)} = {fmt(result)}"] + s.history)[:10]
    s.display = fmt(result)
    s.left = None
    s.op = None
    return True


def press_op(op: str):
    s = st.session_state
    s.error = None
    if s.op is not None and not s.fresh:
        if not evaluate():
            return
    s.left = float(s.display)
    s.op = op
    s.fresh = True


def press_equals():
    s = st.session_state
    s.error = None
    if evaluate():
        s.fresh = True


init_state()

st.title("Calculator")

if st.session_state.error:
    st.error(st.session_state.error, icon=":material/error:")

with st.container(border=True):
    pending = f"{fmt(st.session_state.left)} {st.session_state.op}" if st.session_state.op else " "
    st.caption(pending)
    st.header(st.session_state.display, anchor=False, text_alignment="right")

    mode = st.segmented_control(
        "Mode", ["Basic", "Scientific"], default="Basic", key="mode", label_visibility="collapsed"
    )

    if mode == "Scientific":
        sci_rows = [["√", "x²", "1/x", "n!"], ["sin", "cos", "tan", "log"], ["ln"]]
        for r, names in enumerate(sci_rows):
            cols = st.columns(4)
            for c, name in enumerate(names):
                cols[c].button(name, key=f"sci_{r}_{c}", on_click=press_func, args=(name,), width="stretch")
            if r == 2:
                cols[1].button("xʸ", key="sci_pow", on_click=press_op, args=("^",), type="primary", width="stretch")
                cols[2].button("mod", key="sci_mod", on_click=press_op, args=("mod",), type="primary", width="stretch")
                cols[3].button("π", key="sci_pi", on_click=press_pi, width="stretch")

    # (label, callback, args, type)
    rows = [
        [("AC", clear_all, (), "secondary"), ("±", press_negate, (), "secondary"),
         ("%", press_percent, (), "secondary"), ("÷", press_op, ("÷",), "primary")],
        [("7", press_digit, ("7",), "secondary"), ("8", press_digit, ("8",), "secondary"),
         ("9", press_digit, ("9",), "secondary"), ("×", press_op, ("×",), "primary")],
        [("4", press_digit, ("4",), "secondary"), ("5", press_digit, ("5",), "secondary"),
         ("6", press_digit, ("6",), "secondary"), ("−", press_op, ("−",), "primary")],
        [("1", press_digit, ("1",), "secondary"), ("2", press_digit, ("2",), "secondary"),
         ("3", press_digit, ("3",), "secondary"), ("+", press_op, ("+",), "primary")],
        [("⌫", press_backspace, (), "secondary"), ("0", press_digit, ("0",), "secondary"),
         (".", press_dot, (), "secondary"), ("=", press_equals, (), "primary")],
    ]

    for r, row in enumerate(rows):
        cols = st.columns(4)
        for c, (label, callback, args, kind) in enumerate(row):
            cols[c].button(
                label,
                key=f"btn_{r}_{c}",
                on_click=callback,
                args=args,
                type=kind,
                width="stretch",
            )

with st.expander("History", expanded=False):
    if st.session_state.history:
        for entry in st.session_state.history:
            st.text(entry)
        st.button("Clear history", on_click=lambda: st.session_state.update(history=[]))
    else:
        st.caption("No calculations yet.")
