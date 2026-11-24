import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return np.exp(x)


def f_prime(x):
    return np.exp(x)


def f_double_prime(x):
    return np.exp(x)


def natural_cubic_spline_coeffs(x, y):
    n = len(x) - 1
    h = np.diff(x)

    # --- 1. Формуємо систему для c_i ---
    A = np.zeros((n + 1, n + 1))
    B = np.zeros(n + 1)

    # Природні граничні умови
    A[0, 0] = 1
    A[n, n] = 1

    for i in range(1, n):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        B[i] = 6 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1])
        equation = (
            f"{A[i, i - 1]:.4f} * c_{i - 1} + "
            f"{A[i, i]:.4f} * c_{i} + "
            f"{A[i, i + 1]:.4f} * c_{i + 1} = "
            f"{B[i]:.4f}"
        )
        print(equation)

    c = np.linalg.solve(A, B)
    print(f"c = {c}")
    a = y.copy()
    d = np.zeros(n)
    b = np.zeros(n)
    print(f"a = {a}")
    for i in range(n):
        if i < n:
            d[i] = (c[i + 1] - c[i]) / h[i]
            b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (2 * c[i] + c[i + 1]) / 6
    print(f"b = {b}")
    print(f"d = {d}")
    return a, b, c, d, h


def spline_eval(x, x_nodes, a, b, c, d, h):
    n = len(x_nodes) - 1
    result = np.zeros_like(x)

    for idx, xx in enumerate(x):
        i = np.searchsorted(x_nodes, xx) - 1
        i = max(0, min(i, n - 1))
        t = xx - x_nodes[i]
        result[idx] = a[i] + b[i] * t + c[i] * t ** 2 / 2 + d[i] * t ** 3 / 6

    return result


def spline_eval_prime(x, x_nodes, b, c, d, h):
    """Перша похідна сплайна: s'(x) = b_i + c_i*t + d_i*t^2/2"""
    n = len(x_nodes) - 1
    result = np.zeros_like(x)

    for idx, xx in enumerate(x):
        i = np.searchsorted(x_nodes, xx) - 1
        i = max(0, min(i, n - 1))
        t = xx - x_nodes[i]
        result[idx] = b[i] + c[i] * t + d[i] * t ** 2 / 2

    return result


def spline_eval_double_prime(x, x_nodes, c, d, h):
    """Друга похідна сплайна: s''(x) = c_i + d_i*t"""
    n = len(x_nodes) - 1
    result = np.zeros_like(x)

    for idx, xx in enumerate(x):
        i = np.searchsorted(x_nodes, xx) - 1
        i = max(0, min(i, n - 1))
        t = xx - x_nodes[i]
        result[idx] = c[i] + d[i] * t

    return result


def main():
    a0, b0 = -1, 1
    n_nodes = 15

    x_nodes = np.linspace(a0, b0, n_nodes)
    y_nodes = f(x_nodes)

    # Коефіцієнти
    a_i, b_i, c_i, d_i, h = natural_cubic_spline_coeffs(x_nodes, y_nodes)

    # Друкуємо поліноми
    print("\nКубічні поліноми сплайна:\n")
    for i in range(len(h)):
        print(f"[{x_nodes[i]:.3f}, {x_nodes[i + 1]:.3f}]:")
        print(f"s{i}(x) = {a_i[i]:.6f} "
              f"+ {b_i[i]:.6f}(x - {x_nodes[i]:.6f}) "
              f"+ {c_i[i] / 2:.6f}(x - {x_nodes[i]:.6f})^2 "
              f"+ {d_i[i] / 6:.6f}(x - {x_nodes[i]:.6f})^3\n")

    # Побудова графіків
    x_plot = np.linspace(a0, b0, 500)
    y_plot = spline_eval(x_plot, x_nodes, a_i, b_i, c_i, d_i, h)
    y_prime_plot = spline_eval_prime(x_plot, x_nodes, b_i, c_i, d_i, h)
    y_double_prime_plot = spline_eval_double_prime(x_plot, x_nodes, c_i, d_i, h)

    # Значення похідних у вузлах
    y_prime_nodes = f_prime(x_nodes)
    y_double_prime_nodes = f_double_prime(x_nodes)

    # Графік функції
    plt.figure(figsize=(18, 5))

    plt.subplot(1, 3, 1)
    plt.plot(x_plot, f(x_plot), label="exp(x)", linewidth=2)
    plt.plot(x_plot, y_plot, '--', label="Сплайн", linewidth=2)
    plt.scatter(x_nodes, y_nodes, color='red', label="Вузли", zorder=5)
    plt.grid(True)
    plt.legend()
    plt.title("Оригінал")
    plt.xlabel("x")
    plt.ylabel("f(x)")

    # Графік першої похідної
    plt.subplot(1, 3, 2)
    plt.plot(x_plot, f_prime(x_plot), label="exp(x)", linewidth=2)
    plt.plot(x_plot, y_prime_plot, '--', label="Сплайн s'(x)", linewidth=2)
    plt.scatter(x_nodes, y_prime_nodes, color='red', label="Вузли", zorder=5)
    plt.grid(True)
    plt.legend()
    plt.title("Перша похідна")
    plt.xlabel("x")
    plt.ylabel("f'(x)")

    # Графік другої похідної
    plt.subplot(1, 3, 3)
    plt.plot(x_plot, f_double_prime(x_plot), label="exp(x)", linewidth=2)
    plt.plot(x_plot, y_double_prime_plot, '--', label="Сплайн s''(x)", linewidth=2)
    plt.scatter(x_nodes, y_double_prime_nodes, color='red', label="Вузли", zorder=5)
    plt.grid(True)
    plt.legend()
    plt.title("Друга похідна")
    plt.xlabel("x")
    plt.ylabel("f''(x)")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()