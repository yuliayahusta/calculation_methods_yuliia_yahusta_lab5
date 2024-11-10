import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def get_function() -> callable:
    """
    Повертає функцію F(x), яку визначає користувач.
    """
    print("Enter the function. For example, the default function is F(x) = 2 * x ** 4 - 8 * x ** 3 - 16 * x ** 2 - 1.")
    user_input = input("F(x) = ")
    return lambda x: eval(user_input, {"x": x})


def F_default(x: float) -> float:
    """
    Стандартна функція для обчислення.
    """
    return 2 * x ** 4 - 8 * x ** 3 - 16 * x ** 2 - 1


def dF(x: float) -> float:
    """
    Похідна функції F(x).
    """
    return 8 * x ** 3 - 24 * x ** 2 - 32 * x


def newtons_method(a, b, e, F, dF):
    roots = []
    intermediate_values = []
    x = a
    i = 0

    while x < b:
        y1 = F(x)
        y2 = F(x + e * 100)

        if (y1 > 0 and y2 < 0) or (y1 < 0 and y2 > 0):
            x1 = x
            n = 0
            previous_x = x1
            while True:
                x2 = x1 - F(x1) / dF(x1)
                f_xn = F(x1)
                df_xn = dF(x1)
                diff = abs(x1 - x2)
                intermediate_values.append([n, x1, f_xn, df_xn, diff])
                if diff <= e:
                    break
                previous_x = x1
                x1 = x2
                n += 1
            roots.append(x1)
            i += 1
        x += e * 100
    return roots, intermediate_values


def main() -> None:
    """
    Головна функція програми: отримує вхідні дані, обчислює результати, виводить таблицю та будує графік.
    """
    print("\nSolving a nonlinear equation using Newton's method")
    print("Default function: F(x) = 2 * x^4 - 8 * x^3 - 16 * x^2 - 1")

    use_default = input("Do you want to continue with this function? (yes/no): ").strip().lower()

    if use_default == "yes":
        F = F_default
    else:
        F = get_function()

    a = float(input("Enter the interval [a; b]:\na (for 18 it`s -2) = "))  # Ask for a
    b = float(input("b (for 18 it`s 6) = "))  # Ask for b
    e = float(input("Enter the error tolerance e (0.0001) = "))  # Error tolerance

    # Find roots and intermediate values
    roots, table_data = newtons_method(a, b, e, F, dF)

    # Output results
    print("\nRoots:")
    for i, root in enumerate(roots):
        print(f"x{i} = {root:.4f}")

    # Print the intermediate table
    print("\nIntermediate values:")
    columns = ["n", "xn", "f(xn)", "f'(xn)", "xn - xn-1"]
    intermediate_table = pd.DataFrame(table_data, columns=columns)
    print(intermediate_table.to_string(index=False))

    # Plot function and roots
    x_vals = np.linspace(a - 1, b + 1, 400)
    y_vals = F(x_vals)

    plt.figure(figsize=(10, 6))

    # Plotting the function
    plt.plot(x_vals, y_vals, color='fuchsia', label="F(x)")
    plt.axhline(0, color="gray", linestyle="--")

    # Filling the area between a and b with light pink color
    x_fill = np.linspace(a, b, 400)
    y_fill = F(x_fill)
    plt.fill_between(x_fill, y_fill, color='fuchsia', alpha=0.3, label=f"Interval [{a}, {b}]")

    # Highlighting the roots
    plt.scatter(roots, [0] * len(roots), color="fuchsia", label="Roots")

    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.title("Plot of F(x) with Roots Indicated and Interval Highlighted")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
