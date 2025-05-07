import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    def p1(n):
        return np.polynomial.polynomial.Polynomial([0]+[(-1)**(n-i+1)/(i+1) for i in range(0,n)])
    print(p1(5))
    return np, p1


@app.cell
def _():
    def fn0_sum(x,n):
        return sum(((-1)**i*x**(n-i)/(n-i) for i in range(0,n)))
        #return np.sum(np.fromiter(((-1)**i*x**(n-i)/(n-i) for i in range(0,n)), float))
    print( fn0_sum(0.5,5))
    return (fn0_sum,)


@app.cell
def _(fn0_sum, p1):
    def fn0(x,n):
        res = 0.
        for i in range(0,n):
            res= res + (-1)**i*x**(n-i)/(n-i)
        return res

    print(p1(5)(0.4), fn0(0.4,5), fn0_sum(0.4,5))
    return (fn0,)


@app.cell
def _(p1):
    N = 1500000
    fp1 = p1(10)
    for i in range(1,N):
        y = fp1(float(i)/N)
    return (N,)


@app.cell
def _(N, fn0, fn0_sum, p1):
    import timeit
    fn_p5 = p1(5)
    print ('fn_p5:', timeit.timeit(lambda :fn_p5(0.5), number=N))
    print ('fn0:', timeit.timeit(lambda :fn0(0.5,5), number=N))
    print ('fn0_sum:', timeit.timeit(lambda :fn0_sum(0.5,5) , number=N))
    return


@app.cell
def _(np):
    def fn1(x,n):
        res = 0.
        for i in range(0,n):
            res = res + (-1)**i*x**(n-i)/(n-i)
        res = res + (-1)**n*np.log(abs(1.+x))
        return res/(1+x)/x**(n+1)

    vfn1 = np.vectorize(fn1)

    def fn2(x,n):
        res = 0.
        for i in range(0,n):
            res = res +(-1)**(n+i+2)*x**(+i)/(n+1+i)
        return res*(-1)**n/(1+x)

    vfn2 = np.vectorize(fn2)

    def fn(x,n):
        eps = 0.05
        #return np.piecewise(x, [x<eps, x>=eps], [fn2, fn1], n)
        return np.piecewise(x, [x<eps, x>=eps], [vfn2, vfn1], n)

    #vfn = np.vectorize(fn)
    return fn, fn2


@app.cell
def _(fn, fn2, np):
    from matplotlib import pyplot as plt

    x=np.linspace(0., 1., 100)
    plt.plot(x, fn(x,5), label='fn')
    plt.plot(x, fn2(x,5), label='fn2')
    plt.legend()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
