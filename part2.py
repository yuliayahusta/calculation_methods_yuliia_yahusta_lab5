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


def bisection_method(a, b, t, F):
    """
    Метод бісекції для знаходження кореня рівняння на інтервалі [a, b].
    a, b - межі інтервалу
    t - точність (похибка)
    F - функція для обчислення значення
    """
    p1 = a
    p2 = b
    p = (p1 + p2) / 2

    roots = []
    n = 0
    intermediate_values = []

    # Виконання методу бісекції
    while abs(F(p)) > t:
        intermediate_values.append([n, p1, p2, p, F(p), p2 - p1])
        if F(p1) * F(p) < 0:
            p2 = p  # Корінь в лівому підінтервалі
        else:
            p1 = p  # Корінь в правому підінтервалі
        p = (p1 + p2) / 2
        n += 1

    # Додавання фінальних значень до таблиці
    intermediate_values.append([n, p1, p2, p, F(p), p2 - p1])
    roots.append(p)
    return roots, intermediate_values


def find_roots(a, b, t, F, precision):
    """
    Знаходження коренів на заданому інтервалі.
    Якщо на інтервалі є два корені, вони обидва будуть знайдені.
    """
    roots = []
    intermediate_values = []

    middle = (a + b) / 2

    # Перевірка кореня в лівій частині інтервалу
    if F(a) * F(middle) < 0:
        root1, intermediate_values1 = bisection_method(a, middle, t, F)
        roots += root1
        intermediate_values += intermediate_values1

    # Перевірка кореня в правій частині інтервалу
    if F(middle) * F(b) < 0:
        root2, intermediate_values2 = bisection_method(middle, b, t, F)
        roots += root2
        intermediate_values += intermediate_values2

    # Виведення проміжних значень
    display_intermediate_table(intermediate_values)

    plot_function_and_roots(a, b, roots, F)

    # Виведення коренів після всіх обчислень з відповідною точністю
    if roots:
        for i, root in enumerate(roots):
            print(f"\nRoot {i + 1} of the equation: x = {root:.{precision}f}")
    else:
        print("No roots in the given interval")


def display_intermediate_table(intermediate_values):
    """
    Виведення таблиці проміжних значень під час виконання методу бісекції.
    """
    print("\nIntermediate values from the bisection method:")
    columns = ["n", "a_n", "b_n", "x_n", "f(x_n)", "b_n - a_n"]
    intermediate_table = pd.DataFrame(intermediate_values, columns=columns)
    print(intermediate_table.to_string(index=False))


def plot_function_and_roots(a, b, roots, F):
    """
    Побудова графіка функції та візуалізація коренів на ньому.
    """
    x_vals = np.linspace(a - 1, b + 1, 400)
    y_vals = F(x_vals)

    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, y_vals, color='fuchsia', label="F(x)")
    plt.axhline(0, color="gray", linestyle="--")

    plt.fill_between(x_vals, y_vals, where=((x_vals >= a) & (x_vals <= b)), color='fuchsia', alpha=0.3)

    plt.scatter(roots, [0] * len(roots), color="fuchsia", label="Roots")

    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.title("Plot of F(x) with Roots")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    """
    Головна функція програми: отримує вхідні дані, обчислює корінь рівняння,
    виводить проміжні таблиці та будує графік.
    """
    print("\nSolution of the nonlinear equation using the bisection method: \n")
    print("2*x^4 - 8*x^3 - 16*x^2 - 1 = 0\n")

    use_default = input(
        "Do you want to use the default function? (yes/no): ").strip().lower()

    if use_default == "yes":
        F = F_default
    else:
        F = get_function()

    a = float(input("Enter the interval [a; b]:\na (for 18 it`s -2) = "))
    b = float(input("b (for 18 it`s 6) = "))
    t = float(input("Enter the tolerance e (0.0001) = "))

    # Визначення кількості знаків після коми на основі точності
    precision = len(str(t).split('.')[1]) if '.' in str(t) else 0

    # Знаходження коренів та відображення результатів
    find_roots(a, b, t, F, precision)


if __name__ == "__main__":
    main()
