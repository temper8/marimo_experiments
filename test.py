import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    a = 3
    b = 4
    a + b
    return


if __name__ == "__main__":
    app.run()

