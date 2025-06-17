import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import config as cfg
    ip = cfg.get_initial_path()
    return cfg, ip


@app.cell
def _(ip):
    import marimo as mo
    file_browser = mo.ui.file_browser(initial_path=ip, selection_mode='directory', multiple= False)
    file_browser

    return file_browser, mo


@app.cell
def _(cfg, file_browser):
    race_path = file_browser.path(index=0)
    with race_path.joinpath('done_tasks.txt').open("r") as file:
       done_tasks = [line.strip() for line in file.readlines()]
       print(done_tasks)
    cfg.set_initial_path(str(race_path.parents[0]))
    return done_tasks, race_path


@app.function
def read_power_balance(path):
    pb = {}
    with path.joinpath('PowerBalance.dat').open("r") as file:
        content = [line.strip().split() for line in file.readlines()]
        for line in content:
            pb[line[0]] = float(line[2])
    return pb


@app.cell
def _(done_tasks, race_path):
    tasks_data =[]
    for task in done_tasks:
        pb = read_power_balance(race_path.joinpath(task))
        pb['task'] = task
        tmp = task.split('_')
        pb[tmp[0]] = int(tmp[1])
        tasks_data.append(pb)
        #print(pb)

    return (tasks_data,)


@app.cell
def _():
    #table = mo.ui.table(data=tasks_data, pagination=True)
    #mo.vstack([table, table.value])
    return


@app.cell
def _(tasks_data):
    import pandas as pd
    df = pd.DataFrame.from_dict(tasks_data)
    df
    return (df,)


@app.cell
def _(df, mo):
    import altair as alt
    chart = mo.ui.altair_chart(alt.Chart(df).mark_point().encode(
        x='Nr',
        y='Pabs(kW)'
    ))
    return (chart,)


@app.cell
def _(chart, mo):
    mo.vstack([chart, mo.ui.table(chart.value)])
    return


if __name__ == "__main__":
    app.run()
