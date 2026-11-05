"""Student Grade Manager (Streamlit).

Run with:  streamlit run grade_app.py   (on this PC: python -m streamlit run grade_app.py)

Why session_state? Streamlit reruns this whole script on every click. A plain
`students = []` at the top is recreated empty on every rerun, so each new
student would wipe the previous one. st.session_state survives the reruns.
"""

import streamlit as st


def get_grade(mark: int) -> str:
    """Grading scale from Day 2."""
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "F"


st.set_page_config(page_title="Student grade manager", page_icon=":material/school:")

# Create the list once; it is kept between reruns.
if "students" not in st.session_state:
    st.session_state.students = []

st.title("Student grade manager")

with st.form("add", clear_on_submit=True):
    name = st.text_input("Name")
    # min/max stop marks outside 0-100 right in the interface
    mark = st.number_input("Mark", min_value=0, max_value=100, value=0, step=1)
    submitted = st.form_submit_button("Add", type="primary")

if submitted:
    if not name.strip():
        st.error("Please enter a name.", icon=":material/error:")
    elif not 0 <= mark <= 100:
        st.error("Mark must be between 0 and 100.", icon=":material/error:")
    else:
        st.session_state.students.append({"Name": name.strip(), "Mark": int(mark)})
        st.toast(f"Added {name.strip()}", icon=":material/check:")

students = st.session_state.students

if students:
    marks = [s["Mark"] for s in students]

    average, highest, lowest = st.columns(3)
    average.metric("Class average", f"{sum(marks) / len(marks):.1f}")
    highest.metric("Highest", max(marks))
    lowest.metric("Lowest", min(marks))

    # A Markdown table: a real table on the page that needs no pandas
    # (st.table/st.dataframe import pandas, which is broken on this PC).
    lines = ["| Name | Mark | Grade |", "|---|---:|:---:|"]
    for s in students:
        lines.append(f"| {s['Name'].replace('|', '/')} | {s['Mark']} | {get_grade(s['Mark'])} |")
    st.markdown("\n".join(lines))
else:
    st.info("No students yet. Add one above.")
