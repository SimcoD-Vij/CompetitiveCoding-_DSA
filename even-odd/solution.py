
---

## 🐍 even_or_odd.py  

```python
def check_even_or_odd(n):
    """
    Function to check whether the given input is an even or odd number.
    Handles edge cases:
    - Integer values (works fine)
    - Float values (only accepts if it's like 69.0, rejects 69.69)
    - String numbers ("42" works, "ABC" is rejected)
    """

    try:
        # Convert input to float first (to handle "69.0" and "69")
        num = float(n)

        # Check if it's really an integer (not 69.69)
        if num.is_integer():
            num = int(num)  # Safe to cast
            if num % 2 == 0:
                print(f"{num} is an even number.")
            else:
                print(f"{num} is an odd number.")
        else:
            print("Please enter only integers (decimal numbers are not valid).")

    except Exception:
        print("Please enter only integers.")


# Example test cases
if __name__ == "__main__":
    test_inputs = [69, "42", 69.69, "69.0", "ABC"]
    for inp in test_inputs:
        print(f"Input: {inp}")
        check_even_or_odd(inp)
        print("-" * 40)
