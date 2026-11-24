import numpy as np
from typing import Tuple

def print_matrix(A: np.ndarray, b: np.ndarray):
    for i in range(len(b)):
        row_str = " ".join(f"{A[i, j]:7.2f}" for j in range(A.shape[1]))
        print(f"[{row_str} | {b[i]:7.2f}]")

def generate_universal_matrix(n: int = 4, max_val: int = 9) -> Tuple[np.ndarray, np.ndarray]:

    max_attempts = 100
    for attempt in range(max_attempts):
        A = np.zeros((n, n))

        # Заповнюємо верхній трикутник
        for i in range(n):
            for j in range(i + 1, n):
                A[i, j] = np.random.randint(-max_val // 2, max_val // 2 + 1)

        # Дублюємо у нижній трикутник для симетричності
        A = A + A.T

        # Забезпечуємо діагональну домінантність
        for i in range(n):
            row_sum = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
            A[i, i] = row_sum + np.random.randint(2, max_val // 2 + 1)

        # Перевіряємо, чи всі елементи за модулем < 10
        if np.any(np.abs(A) >= 10):
            continue

        # Перевіряємо позитивну визначеність
        try:
            eigenvalues = np.linalg.eigvals(A)
            if np.any(eigenvalues <= 1e-10):
                continue
        except:
            continue

        # Перевіряємо ненульовий визначник
        det_A = np.linalg.det(A)
        if abs(det_A) < 1e-10:
            continue


        b = np.random.randint(-max_val, max_val + 1, n).astype(float)

        return A, b

    raise ValueError(f"Не вдалося згенерувати матрицю за {max_attempts} спроб")



def gauss_elimination_rows(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = len(b)
    A = A.copy()
    b = b.copy()
    perm = np.arange(n)

    print("\nХід методу Гауса:")
    print(f"Початкова перестановка: {perm}")

    # Пряме проходження
    for k in range(n - 1):
        # Вибір головного елемента по рядках (по k-му рядку)
        max_col = k
        for j in range(k + 1, n):
            if abs(A[k, j]) > abs(A[k, max_col]):
                max_col = j

        # Перестановка стовпців
        if max_col != k:
            A[:, [k, max_col]] = A[:, [max_col, k]]
            perm[k], perm[max_col] = perm[max_col], perm[k]
            print(f"Крок {k + 1}: переставлено стовпці {k} ↔ {max_col}, "
                  f"перестановка: {perm}")
            print_matrix(A,b)


        print(f"Крок: {k+1}")
        for i in range(k + 1, n):
            factor = A[i, k] / A[k, k]
            A[i, k:] -= factor * A[k, k:]
            b[i] -= factor * b[k]
        print_matrix(A,b)


    # Зворотний хід
    x_perm = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x_perm[i] = (b[i] - np.dot(A[i, i + 1:], x_perm[i + 1:])) / A[i, i]

    # Відновлюємо правильний порядок змінних
    x = np.zeros(n)
    for i in range(n):
        x[perm[i]] = x_perm[i]

    print(f"Фінальна перестановка: {perm}")
    print(f"x (переставлений): {x_perm}")
    print(f"x (відновлений):   {x}")

    return x


def solve_square_root(A: np.ndarray, b: np.ndarray) -> np.ndarray:
    n = len(b)
    A = A.copy()
    b = b.copy()
    S = np.eye(n)
    D = np.zeros(n)

    for i in range(n):
        sum_sq = sum(S[k, i] ** 2 * D[k] for k in range(i))
        D[i] = np.sign(A[i, i] - sum_sq)

        value_under_sqrt = abs(A[i, i] - sum_sq)
        # if value_under_sqrt < 1e-10:
        #     raise ValueError(f"Матриця не є позитивно визначеною на кроці {i}")

        S[i, i] = np.sqrt(value_under_sqrt)

        for j in range(i + 1, n):
            sum_prod = sum(S[k, i] * D[k] * S[k, j] for k in range(i))
            S[i, j] = (A[i, j] - sum_prod) / (D[i] * S[i, i])

    print(f"D: {D}")
    print(f"S: {S}")

    # Знаходимо у
    y = np.zeros(n)
    for i in range(n):
        sum_val = sum(S[j, i] * D[j] * y[j] for j in range(i))
        y[i] = (b[i] - sum_val) / (S[i, i] * D[i])
    print(f"Y: {y}")

    # Знаходимо х
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        sum_val = sum(S[i, j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - sum_val) / S[i, i]

    print(f"X: {x}")

    return x


def jacobi_method(A: np.ndarray, b: np.ndarray, tol: float = 1e-6,
                  max_iter: int = 1000) -> Tuple[np.ndarray, int]:
    n = len(b)
    A = A.copy()
    b = b.copy()
    x = np.zeros(n)
    x_new = np.zeros(n)

    for iteration in range(max_iter):
        for i in range(n):
            sum_val = np.dot(A[i, :], x) - A[i, i] * x[i]
            x_new[i] = (b[i] - sum_val) / A[i, i]
        print(f"Ітерація: {iteration + 1}")
        print(f"X: {x_new}")
        print(f"Перевірка критерію зупинки: {np.linalg.norm(x_new - x, ord=np.inf)}")

        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, iteration + 1

        x = x_new.copy()

    print(f"Попередження: метод не збігся за {max_iter} ітерацій")
    return x_new, max_iter





def main():
    print("=" * 70)
    print("РОЗВ'ЯЗАННЯ СИСТЕМ ЛІНІЙНИХ АЛГЕБРАЇЧНИХ РІВНЯНЬ")
    print("=" * 70)

    # Генерація матриці
    # print("\n1. ГЕНЕРАЦІЯ МАТРИЦІ")
    # A, b = generate_universal_matrix()
    # print_matrix(A, b)
    A = np.array([
        [9, 2, -3, -1],
        [2, 8, 1, -2],
        [-3, 1, 7, 0],
        [-1, -2, 0, 6]
    ], dtype=float)

    b = np.array([5, 8, 1, 3], dtype=float)

    # Метод Гауса з вибором головного по рядках
    print("\n" + "=" * 70)
    print("2. МЕТОД ГАУСА (вибір головного елемента по рядках)")
    print("=" * 70)
    gauss_elimination_rows(A, b)

    # Метод квадратного кореня
    print("\n" + "=" * 70)
    print("3. МЕТОД КВАДРАТНОГО КОРЕНЯ")
    print("=" * 70)
    solve_square_root(A, b)

    # Метод Якобі
    print("\n" + "=" * 70)
    print("4. МЕТОД ЯКОБІ")
    print("=" * 70)

    while True:
        try:
            tol_input = input("\nВведіть точність або Enter для 1e-6: ").strip()
            tolerance = float(tol_input) if tol_input else 1e-6
            if tolerance <= 0:
                print("Точність повинна бути додатною!")
                continue
            break
        except ValueError:
            print("Некоректне значення!")

    x_jacobi, iterations = jacobi_method(A, b, tol=tolerance)
    print(f"\nКількість ітерацій: {iterations}")



if __name__ == "__main__":
    main()