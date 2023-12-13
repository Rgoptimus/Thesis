import streamlit as st

def calculate_sgpa(grades):
    credit_points = {"A": 4, "AB": 3.5, "B": 3, "BC": 2.5, "C": 2, "D": 1}

    total_credit = 0
    total_marks = 0

    for grade in grades:
        credit = credit_points.get(grade, 0)
        total_credit += credit
        total_marks += credit * 10

    sgpa = total_marks / len(grades) / 10
    return sgpa

def main():
    st.title("SGPA Calculator")

    # Input for grades
    grades = st.text_input("Enter grades separated by spaces (e.g., A B AB):").split()

    if grades:
        # Calculate SGPA
        sgpa = calculate_sgpa(grades)

        # Display results
        st.success(f"SGPA: {sgpa:.2f}")

if __name__ == "__main__":
    main()
