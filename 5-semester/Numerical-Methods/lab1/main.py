from tabulate import tabulate
import math


#Метод бісекції
def bisection(f, a, b, eps):
    results = []
    if f(a) * f(b) > 0:
        raise ValueError("На відрізку [a, b] немає кореня або їх парна кількість")
    n1=int(math.log((b-a)/eps,2))
    n=0
    while n<=n1:
        x = (a + b) / 2
        results.append([n, a, b, x, f(x)])

        if f(a) * f(x) < 0:
            b = x
        else:
            a = x
        n+=1

    return results


#Метод релаксації
def relaxation(f, df, x, tau, eps, q0):
    results = []
    n1=int(math.log(0.5/eps, math.e)/math.log(1/q0, math.e)+1)
    n=0
    prev_x = None
    while n<=n1:
        if df(x)>0:
            x_new = x - tau * f(x)
        else:
            x_new = x + tau * f(x)
        if prev_x is not None:
            apost = (q0 / (1 - q0)) * abs(x - prev_x)
        else:
            apost = None
        results.append([n, x, f(x), apost])

        prev_x=x
        x = x_new
        n+=1

    return results


def main():
    # Задана функція
    f = lambda x: x**4+4*x-2
    df = lambda x: 4 * x**3 + 4

    # Параметри
    a, b = 0, 1
    eps = 1e-4
    x0 = 0.5
    tau = 1/6
    q0=1/3

    print("\n=== Метод бісекції ===")
    bis_results = bisection(f, a, b, eps)
    print(tabulate(bis_results, headers=["№", "a", "b", "x", "f(x)"], floatfmt=".6f"))

    print("\n=== Метод релаксації ===")

    rel_results = relaxation(f, df, x0, tau, eps, q0)
    print(tabulate(rel_results, headers=["№", "x", "f(x)", "(q0/(1- q0))*|𝑥n – 𝑥n-1|"], floatfmt=".6f"))


if __name__ == "__main__":
    main()
