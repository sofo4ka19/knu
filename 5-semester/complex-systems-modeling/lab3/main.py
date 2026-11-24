import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Оголошення символів
c1, c2, c3, c4, m1, m2, m3 = sp.symbols("c1 c2 c3 c4 m1 m2 m3")


def set_A():
    """Створює символьну матрицю системи"""
    return sp.Matrix([
        [0, 1, 0, 0, 0, 0],
        [-(c1 + c2) / m1, 0, c2 / m1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [c2 / m2, 0, -(c2 + c3) / m2, 0, c3 / m2, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, c3 / m3, 0, -(c3 + c4) / m3, 0]
    ])


def compute_y_RK(A, y_prev, dt):
    """Рунге-Кутта 4-го порядку для векторів стану"""
    k1 = dt * (A @ y_prev)
    k2 = dt * (A @ (y_prev + k1 / 2))
    k3 = dt * (A @ (y_prev + k2 / 2))
    k4 = dt * (A @ (y_prev + k3))
    return y_prev + (k1 + 2 * k2 + 2 * k3 + k4) / 6


def compute_U_RK(A, dA_dy_vec, U_prev, dt):
    """
    Рунге-Кутта для матриці чутливості
    dA_dy_vec: вектор [∂(Ay)/∂β₁, ∂(Ay)/∂β₂, ..., ∂(Ay)/∂βₙ] розміром (6, n_params)
    """
    k1 = dt * (A @ U_prev + dA_dy_vec)
    k2 = dt * (A @ (U_prev + k1 / 2) + dA_dy_vec)
    k3 = dt * (A @ (U_prev + k2 / 2) + dA_dy_vec)
    k4 = dt * (A @ (U_prev + k3) + dA_dy_vec)
    return U_prev + (k1 + 2 * k2 + 2 * k3 + k4) / 6


def simulate_model(A_num, y_0, dt, n_steps):
    """Моделює систему з заданими параметрами"""
    y_trajectory = np.zeros((6, n_steps))
    y_trajectory[:, 0] = y_0

    for i in range(1, n_steps):
        y_trajectory[:, i] = compute_y_RK(A_num, y_trajectory[:, i - 1], dt)

    return y_trajectory


def to_vector(beta_dict, beta_symbols):
    """Перетворює словник параметрів у вектор"""
    return np.array([float(beta_dict[sym]) for sym in beta_symbols])


def to_dict(beta_vec, beta_symbols):
    """Перетворює вектор параметрів у словник"""
    return {sym: float(val) for sym, val in zip(beta_symbols, beta_vec)}


def computation(A_sym, A_known_par, beta_symbols, beta_0, y_obs, epsilon, dt, T):
    """
    Основна функція ідентифікації параметрів
    """
    MAX_ITER = 100
    n_params = len(beta_symbols)
    y_0 = y_obs[:, 0].copy()
    beta_cur = beta_0.copy()

    # Для зберігання історії
    history = {
        'iterations': [],
        'quality': [],
        'params': []
    }

    # Попереднє обчислення символьних похідних dA/dβᵢ
    print("Обчислення символьних похідних матриці A...")
    dA_list = [sp.diff(A_known_par, param) for param in beta_symbols]

    for iter_num in range(1, MAX_ITER + 1):
        # Підстановка поточних значень параметрів
        A_num = np.array(A_known_par.subs(beta_cur)).astype(float)
        dA_list_num = [np.array(dA.subs(beta_cur)).astype(float) for dA in dA_list]

        # Ініціалізація
        y_i = y_0.copy()
        U = np.zeros((6, n_params))

        integral_inv = np.zeros((n_params, n_params))
        integral_u_y = np.zeros(n_params)
        integral_distance = 0.0

        # Інтегрування по часу
        for i in range(y_obs.shape[1]):
            if i > 0:
                # Крок інтегрування для y
                y_i = compute_y_RK(A_num, y_i, dt)

                # Обчислення ∂(Ay)/∂β для поточного y_i
                dA_dy_vec = np.column_stack([dA @ y_i for dA in dA_list_num])

                # Крок інтегрування для U
                U = compute_U_RK(A_num, dA_dy_vec, U, dt)

            # Обчислення інтегралів
            delta_y = y_obs[:, i] - y_i
            integral_inv += (U.T @ U) * dt
            integral_u_y += (U.T @ delta_y) * dt
            integral_distance += (delta_y.T @ delta_y) * dt

        # Зберігаємо історію
        history['iterations'].append(iter_num)
        history['quality'].append(integral_distance)
        history['params'].append(beta_cur.copy())

        # Виведення інформації
        print(f"\n{'=' * 50}")
        print(f"Ітерація {iter_num}")
        print("Поточні параметри:")
        for sym in beta_symbols:
            print(f"  {sym} = {beta_cur[sym]:.6f}")
        print(f"Показник якості I(β) = {integral_distance:.6e}")

        # Перевірка збіжності
        if integral_distance < epsilon:
            print(f"\n✓ Збіжність досягнута! I(β) < ε")
            return beta_cur, history

        # Перевірка вироджденості матриці
        cond_num = np.linalg.cond(integral_inv)
        if cond_num > 1e10:
            print(f"⚠ Увага: погана обумовленість матриці (cond={cond_num:.2e})")

        # Оновлення параметрів
        try:
            delta_b = np.linalg.solve(integral_inv, integral_u_y)
        except np.linalg.LinAlgError:
            print("✗ Помилка: виродження матриці!")
            return beta_cur, history

        print(f"Корекція параметрів: Δβ = {delta_b}")

        beta_vec = to_vector(beta_cur, beta_symbols)
        beta_vec += delta_b
        beta_cur = to_dict(beta_vec, beta_symbols)

        # Перевірка на фізичність параметрів
        if any(val <= 0 for val in beta_vec):
            print("⚠ Увага: отримані нефізичні значення (≤0)!")

    print(f"\n✗ Досягнуто максимальну кількість ітерацій ({MAX_ITER})")
    return beta_cur, history


def plot_results(y_obs, y_initial, y_final, time, history, beta_symbols, beta_0, beta_final):
    """
    Візуалізація результатів ідентифікації - тільки координати
    """
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))

    # Кольори для координат
    colors_obs = ['#2E86AB', '#A23B72', '#F18F01']  # Насичені кольори для спостережень
    coord_names = ['y₁ (позиція маси m₁)', 'y₃ (позиція маси m₂)', 'y₅ (позиція маси m₃)']
    coord_indices = [0, 2, 4]

    # Графіки координат
    for idx, (ax, coord_idx, name, color) in enumerate(zip(axes, coord_indices, coord_names, colors_obs)):

        # Початкова модель (червона пунктирна)
        ax.plot(time, y_initial[coord_idx, :], '--', color='#E63946',
                linewidth=1.5, alpha=0.8, label='Початкова модель', zorder=1)

        # Ідентифікована модель (зелена суцільна)
        ax.plot(time, y_final[coord_idx, :], '-', color='#06A77D',
                linewidth=1.8, label='Ідентифікована модель', zorder=2)

        # Спостереження (точки поверх ліній)
        ax.scatter(time, y_obs[coord_idx, :], s=10, color=color,
                   alpha=0.8, edgecolors='white', linewidth=0.5,
                   label='Спостереження', zorder=3)

        # Оформлення
        ax.set_xlabel('Час, с', fontsize=13, fontweight='bold')
        ax.set_ylabel(name, fontsize=13, fontweight='bold')
        ax.legend(loc='upper right', fontsize=11, framealpha=0.95,
                  shadow=True, fancybox=True)
        ax.grid(True, alpha=0.25, linestyle='--', linewidth=0.8)
        ax.set_xlim([time[0], time[-1]])

        # Рамка
        for spine in ax.spines.values():
            spine.set_linewidth(1.5)

        # Заголовок графіка
        ax.set_title(f'Координата {name}', fontsize=14, fontweight='bold', pad=10)

        # Збільшення товщини міток
        ax.tick_params(axis='both', which='major', labelsize=11, width=1.5, length=6)

    # Загальний заголовок
    fig.suptitle('Параметрична ідентифікація системи коливань трьох мас\n' +
                 f'Ідентифіковані параметри: c₁={beta_final[beta_symbols[0]]:.4f}, ' +
                 f'c₃={beta_final[beta_symbols[1]]:.4f}, m₁={beta_final[beta_symbols[2]]:.4f}',
                 fontsize=15, fontweight='bold', y=0.995)

    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig('identification_results.png', dpi=300, bbox_inches='tight', facecolor='white')
    print("\n📊 Графіки збережено у файл: identification_results.png")
    plt.show()


def main():
    # Завантаження даних
    y_obs = np.loadtxt("y3.txt")
    print(f"Завантажено дані: y3.txt")
    print(f"Розмір даних: {y_obs.shape}")

    # Створення символьної матриці
    A = set_A()

    known_params = [(c2, 0.3), (c4, 0.12), (m2, 28), (m3, 18)]
    beta_symbols = [c1, c3, m1]
    beta_0 = {c1: 0.1, c3: 0.1, m1: 9}

    A_known_par = A.subs(known_params)

    print(f"\nВідомі параметри: {dict(known_params)}")
    print(f"Початкове наближення: {beta_0}")
    print(f"Інтервал часу: [0, 50], крок dt = 0.2")
    print(f"Точність: ε = 1e-5\n")

    # Моделювання з початковими параметрами
    A_initial = np.array(A_known_par.subs(beta_0)).astype(float)
    y_initial = simulate_model(A_initial, y_obs[:, 0], 0.2, y_obs.shape[1])

    # Виконання ідентифікації
    result, history = computation(
        A_sym=A,
        A_known_par=A_known_par,
        beta_symbols=beta_symbols,
        beta_0=beta_0,
        y_obs=y_obs,
        epsilon=1e-5,
        dt=0.2,
        T=50
    )

    print(f"\n{'=' * 50}")
    print("ФІНАЛЬНИЙ РЕЗУЛЬТАТ:")
    for sym in beta_symbols:
        print(f"  {sym} = {result[sym]:.8f}")

    # Моделювання з ідентифікованими параметрами
    A_final = np.array(A_known_par.subs(result)).astype(float)
    y_final = simulate_model(A_final, y_obs[:, 0], 0.2, y_obs.shape[1])

    # Створення часового вектора
    time = np.arange(0, y_obs.shape[1] * 0.2, 0.2)

    # Візуалізація
    plot_results(y_obs, y_initial, y_final, time, history,
                 beta_symbols, beta_0, result)


if __name__ == "__main__":
    main()