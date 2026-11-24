import numpy as np

n=5
def jacobi_rotation_method(A, eps=0.01, max_iter=1000):
    A = A.copy().astype(float)

    U = np.eye(n)

    def max_offdiag(A):
        max_val = 0
        i_max = 0
        j_max = 1
        for i in range(n):
            for j in range(i+1, n):
                if abs(A[i, j]) > abs(max_val):
                    max_val = A[i, j]
                    i_max, j_max = i, j
        return i_max, j_max, max_val

    print("Початкова матриця A:")
    print(A, "\n")

    for k in range(1, max_iter + 1):

        i, j, aij = max_offdiag(A)

        print(f"--- Ітерація {k} ---")
        print(f"Найбільший |a_ij| = {aij:.6f} при i={i}, j={j}")

        if A[i, i] == A[j, j]:
            phi = np.pi / 4
        else:
            phi = 0.5 * np.arctan(2 * A[i, j] / (A[i, i] - A[j, j]))

        cos_phi = np.cos(phi)
        sin_phi = np.sin(phi)

        print(f"phi = {phi:.6f}")
        print(f"cos(phi) = {cos_phi:.6f}, sin(phi) = {sin_phi:.6f}")

        Uk = np.eye(n)
        Uk[i, i] = cos_phi
        Uk[j, j] = cos_phi
        Uk[i, j] = sin_phi
        Uk[j, i] = -sin_phi

        print("Матриця обертання U_k:")
        print(Uk)

        A = Uk @ A @ Uk.T
        print("Оновлена матриця A:")
        print(A, "\n")

        U = U @ Uk

        print(f"Критерій зупинки = {np.sum((A - np.diag(np.diag(A))) ** 2)}\n")
        if np.sum((A - np.diag(np.diag(A))) ** 2) <= eps:
            print("\nДосягнуто потрібної точності.\n")
            break

    print("=== Результат ===")
    print("Власні значення:")
    print(np.diag(A))

    print("\nМатриця власних векторів U:")
    print(U)

    return np.diag(A), U, A


def main():
    A = np.array([
        [4, 1, -2, 0, 3],
        [1, 5, 2, -1, 0],
        [-2, 2, 6, 1, -3],
        [0, -1, 1, 3, 2],
        [3, 0, -3, 2, 7]
    ])

    jacobi_rotation_method(A, eps=0.01)


if __name__ == "__main__":
    main()
