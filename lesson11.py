import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    df = pd.read_csv('output1.dat',sep='\\s+',  header=None, names= ['theta', 'v', 'f'] )
    #df
    return (df,)


@app.cell
def _(df):
    import numpy as np

    # Create the mesh in polar coordinates and compute corresponding Z.

    th = np.resize(df['theta'],(100,100))
    R =  np.resize(df['v'],(100,100))
    #Z = ((R**2 - 1)**2)
    Z = np.resize(df['v'],(100,100))
    # Express the mesh in the cartesian system.
    #X, Y = z*np.cos(P), R*np.sin(P)
    X, Y = R*np.cos(th), R*np.sin(th)
    return X, Y, Z


@app.cell
def _(X, Y, Z):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=1, cols=2,
                        specs=[[{'is_3d': True}, {'is_3d': True}]],
                        subplot_titles=['Bp', 'Sin B'],
                        )

    scene1=dict(aspectratio=dict(x=1, y=2, z=0.5),
                    camera_eye=dict(x=-1.57, y=1.36, z=0.58))

    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorbar_x=-0.07), 1, 1)
    #fig.add_trace(go.Surface(x=X, y=Y, z=Si), 1, 2)
    fig.update_scenes( 
                    aspectratio=dict(x=1, y=1, z=0.6),
                    camera_eye=dict(x=-2.57, y=1.36, z=0.58), row=1, col=1)

    fig.update_scenes( 
                    aspectratio=dict(x=1, y=1, z=0.4),
                    camera_eye=dict(x=-2.57, y=1.36, z=0.58), row=1, col=2)
    fig.update_layout( title_text="Tor",
          autosize=False,
          width=800,
          height=500,
  
    )
    fig.show()
    return


if __name__ == "__main__":
    app.run()
