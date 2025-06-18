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


@app.cell
def _(race_path):
    import configparser
    params = configparser.ConfigParser(inline_comment_prefixes=('#',))
    params.read(race_path.joinpath('calc_params.ini'))
    def print_params(params):
        for section in params.sections():
            print(f"[{section}]")
    return (params,)


@app.cell
def _():
    return


@app.function
def read_power_balance(path):
    pb = {}
    with path.joinpath('power_balance.dat').open("r") as file:
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
    return df, pd


@app.cell
def _(df, params):
    from matplotlib import pyplot as plt
    plt.plot(df[params['series']['var']], df['Pabs(kW)'] , label='Pabs(kW)')
    plt.xlabel(params['series']['var'])
    plt.ylabel('Pabs(kW)')
    plt.legend()
    plt.show()
    return (plt,)


@app.cell(disabled=True)
def _(mo):
    mo.md(
        r"""
    rhoi(i)/a0,&   ! psi - normalised flux coordinate [0,1]
    dV,&           ! flux tube volume (cm^3)
    (PabsLD(i)+PabsTT(i)+PabsMX(i))*drhoi(i-1),& ! power absorbed in flux tube
    PabsLD(i)/Ss,& ! These are absorbed power densities p (kW/cm^3)
    PabsTT(i)/Ss,& ! Power absorbed in the flux tube dP = Pabs*drho,
    PabsMX(i)/Ss   ! so p = dP/dV = (Pabs*drho)/(Ss*drho) = Pabs/Ss
    """
    )
    return


@app.cell
def _(done_tasks, params, pd, plt, race_path):
    if params['series']['var'] == 'Nr':
        title = params['common']['name'] + ' Mmax=' + params['w2grid']['Mmax']
    else:
        title = params['common']['name'] +' Nr=' + params['w2grid']['Nr'] 
    fig, ax = plt.subplots()
    fig.suptitle(title)
    for task1 in done_tasks:
        #pb = read_power_balance(race_path.joinpath(task))
        pabs_psi = race_path.joinpath(task1).joinpath('pabs(psi).dat')
        df1 = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        #plt.plot( df['b'] , label='b')
        #plt.legend()
        #plt.show()
        ax.plot(df1['psi'], df1['Pabs']/df1['dV'] , label=task1)

        #print(df1.index)
    ax.legend()
    ax.set_xlabel('psi')
    ax.set_ylabel('Pabs/dV')
    plt.show()
    return


if __name__ == "__main__":
    app.run()
