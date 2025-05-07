import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import io
    import numpy as np
    import pandas as pd
    plasma = {}
    with open('plasma3.dat') as file:
        chunks = {}
        for l in file.readlines():
            if l.startswith('#'):
                output = io.StringIO()
                chunks[l[1:-1]] = output
            else:
                output.write(l)

        for key, o in chunks.items():     
            o.seek(0)
            df = pd.read_csv(o,  sep='\\s+')
            o.close()
            plasma[key] = df
    return np, plasma


@app.cell
def _(np, plasma):
    from Field import Field
    field = Field(plasma)

    r = np.linspace(0.01, 1.0, 50)
    p = np.linspace(0, 2*np.pi, 50)
    R, P = np.meshgrid(r, p)
    Bt, Bp, Si = field.value(R,P)
    X, Y = field.mag_surf(R,P)
    return (field,)


@app.cell
def _(field, np):
    from scipy.spatial import Delaunay
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    def tri_indices(simplices):
        #simplices is a numpy array defining the simplices of the triangularization
        #returns the lists of indices i, j, k

        return ([triplet[c] for triplet in simplices] for c in range(3))



    def create_tor_mesh(r= 1, cmin=0, cmax=1):
        theta = np.linspace(0, 2*np.pi, 30)
        phi   = np.linspace(0, 1.5*np.pi, 20)

        u,v = np.meshgrid(theta,phi)
        u = u.flatten()
        v = v.flatten()

        Bt, Bp, Si = field.value(r,u)
        x, y, z, = field.mag_surf3D(r, u, v)

        points2D = np.vstack([u,v]).T
        tri = Delaunay(points2D)
        I, J, K = tri_indices(tri.simplices)

        return go.Mesh3d( alphahull= 1,
                        x=x, y=y, z=z,
                        i=I, j=J, k=K,  
                        cmin= cmin, cmax= cmax,
                        intensity = Si, 
                        intensitymode='vertex',
                        flatshading= False,

                        opacity=0.80)
    return create_tor_mesh, go


@app.cell
def _(field, go, np):
    def create_test_line(r):
        theta = np.linspace(0, 2*np.pi, 50)
        phi   = np.linspace(0, 2*np.pi, 50)
        x, y, z, = field.mag_surf3D(r, theta, phi)
        return go.Scatter3d(
        x=x, y=y, z=z,
        mode= 'lines',
        line=dict(
            color='darkblue',
            width=5
        ))

    def mag_line2D(r,n):
          #theta = np.linspace(0, 2*np.pi, 50)
        phi_l   = np.linspace(0, n*np.pi, n*50)
        phi = 0.0
        theta = 0.0
        d_phi = 2*np.pi/50
        theta_l = []
        for phi in phi_l:
            Bt, Bp, Si = field.value(r, theta)
            d_theta = Si * d_phi
            theta = theta + d_theta
            theta_l.append(theta)
        return np.array(theta_l), phi_l


    def create_mag_line(r, n):
        theta, phi = mag_line2D(r,n)
        x, y, z, = field.mag_surf3D(r, theta, phi)
    
        return go.Scatter3d(
            x=x, y=y, z=z,
            opacity=0.2,
            mode= 'lines',
            line=dict(
                color='darkblue',
                width=5
            ))
    return (create_mag_line,)


@app.cell
def _(create_mag_line, create_tor_mesh, go):

    tor1 = create_tor_mesh(r= 1.0, cmin= 0, cmax= 0.2)
    tor2 = create_tor_mesh(r= 0.75, cmin= 0, cmax= 0.2)
    tor3 = create_tor_mesh(r= 0.5, cmin= 0, cmax= 0.2)
    tor4 = create_tor_mesh(r= 0.25, cmin= 0, cmax= 0.2)
    tor5 = create_tor_mesh(r= 0.05, cmin= 0, cmax= 0.2)
    #line1 = create_test_line(1.0)
    line1 = create_mag_line(1.0, 100)
    #line2 = create_mag_line(0.25, 1*248) 

    fig = go.Figure(data=[tor1, tor2,  tor3, tor4, tor5, line1])

    fig.update_layout( title_text="Tor",
          autosize=False,
          width=900,
          height=500,
  
    )
    fig.show()
    return


if __name__ == "__main__":
    app.run()
