import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, expand, lambdify, latex, diff, sstr, N
from math import factorial
import textwrap

def f(x):
    return np.exp(x)

def f_derivative(x, n=1):
    return np.exp(x)

# Інтерполяція методом Лагранжа
def lagrange_interpolation(x_nodes, y_nodes):
    x = symbols('x')
    n = len(x_nodes)
    polynomial = 0
    precision=6

    for i in range(n):
        # Базисний поліном Лагранжа
        L_i = 1
        for j in range(n):
            if i != j:
                L_i *= (x - x_nodes[j])/(x_nodes[i] - x_nodes[j])
        polynomial += y_nodes[i] * L_i
        L_i_fmt = f"{N(L_i, precision)}"
        contrib_fmt = f"{N(y_nodes[i] * L_i, precision)}"
        print(f"Добуток L_{i}(x)")
        print(textwrap.fill(sstr(L_i_fmt), width=150))
        print(f"Внесок y[{i}] * L_{i}(x) =")
        print(textwrap.fill(sstr(contrib_fmt), width=150))

    polynomial = expand(polynomial)
    f_lagrange = lambdify(x, polynomial, 'numpy')

    return polynomial, f_lagrange


# Розділені різниці для методу Ерміта
def divided_differences_hermite(x_nodes, y_nodes, derivatives_data):
    # групуємо похідні за точками
    deriv_dict = {}
    for x_d, order, value in derivatives_data:
        deriv_dict.setdefault(x_d, {})[order] = value

    # формуємо розширений масив вузлів
    z = []
    fz = []

    for x, y in zip(x_nodes, y_nodes):
        # завжди додаємо перший вузол
        z.append(x)
        fz.append(y)

        # скільки разів дублювати?
        if x in deriv_dict:
            max_order = max(deriv_dict[x].keys())
            for k in range(max_order):
                z.append(x)
                # значення дубльованих вузлів = значення функції
                fz.append(y)

    n = len(z)
    F = np.zeros((n, n))

    # перша колонка
    for i in range(n):
        F[i][0] = fz[i]

    # заповнення таблиці
    for j in range(1, n):
        for i in range(n - j):
            if abs(z[i] - z[i+j]) < 1e-10:
                # кратний вузол → беремо похідну
                order = j
                x = z[i]
                if x in deriv_dict and order in deriv_dict[x]:
                    F[i][j] = deriv_dict[x][order] / factorial(order)
                else:
                    F[i][j] = f_derivative(x, order) / factorial(order)
            else:
                F[i][j] = (F[i+1][j-1] - F[i][j-1]) / (z[i+j] - z[i])
    np.set_printoptions(
        threshold=np.inf,
        linewidth=170
    )
    print(F)
    return z, F[0, :]


def hermite_interpolation(x_nodes, y_nodes, derivatives_data):
    x = symbols('x')

    # Обчислюємо розділені різниці
    z, coeffs = divided_differences_hermite(x_nodes, y_nodes, derivatives_data)

    polynomial = coeffs[0]
    product_term = 1
    for i in range(1, len(coeffs)):
        product_term *= (x - z[i - 1])
        polynomial += coeffs[i] * product_term

    print(f"polynom = ")
    print(textwrap.fill(sstr(polynomial.evalf(6)), width=150))

    # Розкриваємо поліном
    polynomial = expand(polynomial)

    # Створюємо числову функцію
    f_hermite = lambdify(x, polynomial, 'numpy')

    return polynomial, f_hermite


def format_polynomial(poly, method_name):
    poly_str = str(poly)
    print(f"\n{method_name}:")
    print("P(x) =", textwrap.fill(sstr(poly.evalf(6)), width=120))



# Основна частина програми
def main():
    # Проміжок та вузли інтерполяції
    a, b = -1, 1
    n_nodes = 15

    # Вузли інтерполяції (рівномірна сітка)
    x_nodes = np.linspace(a, b, n_nodes)
    y_nodes = f(x_nodes)

    # Точки для побудови графіків
    x_plot = np.linspace(a, b, 500)
    y_exact = f(x_plot)

    print("=" * 80)
    print("ІНТЕРПОЛЯЦІЯ ФУНКЦІЇ exp(x) НА ПРОМІЖКУ [-1, 1]")
    print("=" * 80)
    print(f"Кількість вузлів інтерполяції: {n_nodes}")
    print(f"Вузли: {x_nodes}")

    # ==================== МЕТОД ЛАГРАНЖА ====================
    print("\n" + "=" * 80)
    print("МЕТОД ЛАГРАНЖА")
    print("=" * 80)

    poly_lagrange, f_lagrange = lagrange_interpolation(x_nodes, y_nodes)
    format_polynomial(poly_lagrange, "Поліном Лагранжа")

    y_lagrange = f_lagrange(x_plot)

    # ==================== МЕТОД ЕРМІТА ====================
    print("\n" + "=" * 80)
    print("МЕТОД ЕРМІТА")
    print("=" * 80)

    # Вузли для похідних
    indices_order_1 = np.linspace(0, len(x_nodes) - 1, 11, dtype=int)
    nodes_order_1 = x_nodes[indices_order_1]  # 1-й порядок – 11 вузлів
    nodes_order_2 = nodes_order_1[::2]  # 2-й порядок (6 вузлів)
    nodes_order_3 = nodes_order_2[::2]  # 3-й порядок (3 вузли)

    derivatives_data = []

    # 1-й порядок
    for x_d in nodes_order_1:
        derivatives_data.append((x_d, 1, f_derivative(x_d, 1)))

    # 2-й порядок
    for x_d in nodes_order_2:
        derivatives_data.append((x_d, 2, f_derivative(x_d, 2)))

    # 3-й порядок
    for x_d in nodes_order_3:
        derivatives_data.append((x_d, 3, f_derivative(x_d, 3)))

    # Перевірка
    print(f"Кількість умов на похідні: {len(derivatives_data)}")
    for order in [1, 2, 3]:
        pts = [x for x, o, _ in derivatives_data if o == order]
        print(f"  - {order}-го порядку: {len(pts)} (у точках: {pts})")

    poly_hermite, f_hermite = hermite_interpolation(x_nodes, y_nodes, derivatives_data)
    format_polynomial(poly_hermite, "Поліном Ерміта")

    y_hermite = f_hermite(x_plot)

    # ==================== ГРАФІКИ ====================
    # Графік для методу Лагранжа
    plt.figure(figsize=(18, 5))

    plt.subplot(1, 2, 1)
    plt.plot(x_plot, y_exact, 'k-', linewidth=2.5, label='Оригінальна функція exp(x)')
    plt.plot(x_nodes, y_nodes, 'ro', markersize=8, label='Обрані точки (табличні)', zorder=5)
    plt.plot(x_plot, y_lagrange, color='lightgreen', linestyle='--', linewidth=2, alpha=0.8, label='Поліном Лагранжа')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Метод Лагранжа', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    # Графік для методу Ерміта
    plt.subplot(1, 2, 2)
    plt.plot(x_plot, y_exact, 'k-', linewidth=2.5, label='Оригінальна функція exp(x)')
    plt.plot(x_nodes, y_nodes, 'ro', markersize=8, label='Обрані точки (табличні)', zorder=5)
    plt.plot(x_plot, y_hermite, color='pink', linestyle='--', linewidth=2, alpha=0.8, label='Поліном Ерміта')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Метод Ерміта', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('interpolation_methods.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Графік для похідних
    plt.figure(figsize=(18, 5))

    x = symbols('x')
    hermite_derivative_expr = diff(poly_hermite, x)  # перша похідна
    hermite_second_derivative_expr = diff(poly_hermite, x, 2)  # друга похідна
    hermite_third_derivative_expr = diff(poly_hermite, x, 3)  # друга похідна

    # Конвертуємо у функції для numpy
    hermite_derivative_func = lambdify(x, hermite_derivative_expr, 'numpy')
    hermite_second_derivative_func = lambdify(x, hermite_second_derivative_expr, 'numpy')
    hermite_third_derivative_func = lambdify(x, hermite_third_derivative_expr, 'numpy')

    plt.subplot(1, 3, 1)
    plt.plot(x_plot, f_derivative(x_plot, 1), 'k-', linewidth=2.5, label='Перша похідна оригінальної функції exp(x)')
    plt.plot(nodes_order_1, f_derivative(nodes_order_1,1), 'ro', markersize=8, label='Обрані точки (табличні)', zorder=5)
    plt.plot(x_plot, hermite_derivative_func(x_plot), color='lightgreen', linestyle='--', linewidth=2, alpha=0.8, label='Перша похідна поліному Ерміта')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Перша похідна', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 3, 2)
    plt.plot(x_plot, f_derivative(x_plot, 2), 'k-', linewidth=2.5, label='Друга похідна оригінальної функції exp(x)')
    plt.plot(nodes_order_2, f_derivative(nodes_order_2,2), 'ro', markersize=8, label='Обрані точки (табличні)', zorder=5)
    plt.plot(x_plot, hermite_second_derivative_func(x_plot), color='pink', linestyle='--', linewidth=2, alpha=0.8, label='Друга похідна поліному Ерміта')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Друга похідна', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 3, 3)
    plt.plot(x_plot, f_derivative(x_plot, 3), 'k-', linewidth=2.5, label='Третя похідна оригінальної функції exp(x)')
    plt.plot(nodes_order_3, f_derivative(nodes_order_3,3), 'ro', markersize=8, label='Обрані точки (табличні)', zorder=5)
    plt.plot(x_plot, hermite_third_derivative_func(x_plot), color='lightblue', linestyle='--', linewidth=2, alpha=0.8,
             label='Третя похідна поліному Ерміта')
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title('Третя похідна', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('interpolation_methods.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()