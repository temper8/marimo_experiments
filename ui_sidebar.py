import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.hstack(
        [
            mo.vstack([mo.md("..."), mo.ui.text_area()]),
            mo.vstack([mo.ui.checkbox(), mo.ui.text(), mo.ui.date()]),
        ]
    )
    return


@app.cell
def _(mo):
    mo.tree(
        ["entry", "another entry", {"key": [0, 1, 2]}], label="A tree."
    )
    return


@app.cell
def _():
    import config as cfg
    ip = cfg.get_initial_path()
    return (ip,)


@app.cell
def _(ip, mo):
    def on_change_cb(FileBrowserFileInfo):
        pass
        #print(FileBrowserFileInfo[0])

    folder_browser = mo.ui.file_browser(initial_path=ip, 
                                        selection_mode='directory',
                                        label='Base folder',
                                        on_change=on_change_cb,
                                        multiple= False)
    return (folder_browser,)


@app.cell
def _(folder_browser, mo):
    task_browser = mo.ui.file_browser(initial_path=folder_browser.path(index=0), selection_mode='directory', label='Race folder', multiple= False)
    return (task_browser,)


@app.cell
def _(folder_browser, mo, task_browser):
    mo.sidebar(
        [
            mo.md("# Wave 2D"),
            mo.nav_menu(
                {
                    "#home": f"{mo.icon('lucide:home')} Home",
                    "#about": f"{mo.icon('lucide:user')} About",
                    "#contact": f"{mo.icon('lucide:phone')} Contact",
                    "Links": {
                        "https://twitter.com/marimo_io": "Twitter",
                        "https://github.com/marimo-team/marimo": "GitHub",
                    },
                },
                orientation="vertical",
            ),
        mo.accordion(
        {
            "Door 1": folder_browser,
            "Door 2": task_browser,
            "Door 3": mo.md(
                "![goat](https://images.unsplash.com/photo-1524024973431-2ad916746881)"
            ),
        }
        )
                ]
    )

    return


@app.cell
def _(mo):
    mo.md(
        r"""
    The exponential function $f(x) = e^x$ can be represented as

    \[
        f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
    \]
    """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""The exponential function $f(x) = e^x$ can be represented as""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    /// details | Warning details  
        type: warn

    This highlights something to watch out for
    ///
    """
    )
    return


if __name__ == "__main__":
    app.run()
