import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import config as cfg
    ip = cfg.get_initial_path()
    return (ip,)


@app.cell
def _(ip):
    import marimo as mo
    folder_browser = mo.ui.file_browser(initial_path=ip, 
                                        selection_mode='directory',
                                        label='Base folder',
                                        multiple= False)

    return folder_browser, mo


@app.cell
def _(folder_browser, mo):
    race_browser = mo.ui.file_browser(initial_path=folder_browser.path(index=0),
                                      selection_mode='directory',
                                      label='Race folder',
                                      multiple= False)
    return (race_browser,)


@app.cell
def _(mo, race_browser):
    race_path = race_browser.path(index=0)
    if race_path:
        if race_path.joinpath('done_tasks.txt').exists():
            #info = mo.md(f"done_tasks exists")
            info_kind = 'success'
            with race_path.joinpath('done_tasks.txt').open("r") as file:
                done_tasks = [line.strip() for line in file.readlines()]
            info = mo.md(f"{race_path.name}\n\n {done_tasks}")        
        else:
            info = mo.md(f"done_tasks not exists!")
            info_kind = 'danger'
    else:
        info = mo.md(f"Upps2")
        info_kind = 'danger'        
    return info, info_kind


@app.cell
def _(info, info_kind, mo):
    info_bar = mo.callout(info, kind=info_kind)
    return (info_bar,)


@app.cell
def _(folder_browser, info_bar, mo, race_browser):
    mo.vstack([
        mo.hstack([folder_browser, race_browser,]),
        info_bar
    ])

    return


@app.cell
def _():



    return


if __name__ == "__main__":
    app.run()
