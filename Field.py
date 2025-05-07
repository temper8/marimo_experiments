import numpy as np
from Polynom import Polynom

class Field():
    def __init__(self, plasma) -> None:
        self.r0 = plasma['vars']['r0'][0]
        self.rm = plasma['vars']['rm'][0]
        self.z0 = plasma['vars']['z0'][0]
        self.b_tor=np.abs(plasma['vars']['b_tor0'][0])
        self.delta = Polynom(plasma['approx']['cdl'])  # delta - shift as a function of "minor radius"
        self.ell = Polynom(plasma['approx']['cly'])    # ellipticity as a function of "minor radius"
        self.gamma =  Polynom(plasma['approx']['cgm']) # gamma - triangularity as a function of "minor radius":
        self.amy =  Polynom(plasma['approx']['cmy']) # Polinomial approximation of the amy(r) 
                                                     #  amy=(btor/q)*rho*(drho/dr) is a function of "minor radius" r=rh(i).

    def mag_surf(self, r, theta):
        Δ = self.delta.val(r)
        λ = self.ell.val(r)
        γ = self.gamma.val(r)

        cotet=np.cos(theta)
        sitet=np.sin(theta)

        xx = -Δ + r*cotet - γ*sitet**2
        zz = r*λ*sitet

        x = (self.r0 + self.rm*xx)/100
        z = (self.z0 + self.rm*zz)/100
        return x, z

    def mag_surf3D(self, r, theta, phi):
        Δ = self.delta.val(r)
        λ = self.ell.val(r)
        γ = self.gamma.val(r)

        cotet=np.cos(theta)
        sitet=np.sin(theta)
        
        xx = -Δ + r*cotet - γ*sitet**2
        zz = r*λ*sitet

        x = (self.r0 + self.rm*xx)/100
        y = x *np.cos(phi)
        x = x *np.sin(phi)
        z = (self.z0 + self.rm*zz)/100
        return x, y, z

    def mag_surf2(self, xr, theta, delta, ell, gamma):
        xdl = delta
        xly = ell
        xgm = gamma
        cotet=np.cos(theta)
        sitet=np.sin(theta)
        xx=-xdl+xr*cotet-xgm*sitet**2
        zz=xr*xly*sitet
        x=(self.r0 + self.rm*xx)/100
        z=(self.z0 + self.rm*zz)/100
        return x, z

    def value(self, pa, theta):
        xdl  = self.delta.val(pa)
        xdlp = self.delta.der(pa)
        xly  = self.ell.val(pa)
        xlyp = self.ell.der(pa)
        xgm  = self.gamma.val(pa)
        xgmp = self.gamma.der(pa)
        xmy = self.amy.val(pa)
        xlyv = xlyp*pa + xly
        cotet = np.cos(theta)
        sitet = np.sin(theta)
        dxdr = -xdlp + cotet- xgmp*sitet**2
        dxdt = -(pa + 2.0*xgm*cotet)*sitet
        dzdr = xlyv*sitet
        dzdt = xly*pa*cotet
        x0=self.r0/self.rm-xdl+pa*cotet-xgm*sitet**2
        dxdrdt=-sitet-2.0*xgmp*sitet*cotet
        dzdrdt=xlyv*cotet
        dxdtdt=-pa*cotet-2.0*xgm*(cotet**2-sitet**2)
        dzdtdt=-xly*pa*sitet
        x0t=dxdt
        #--------------------------------------
        # components of metric tensor
        #--------------------------------------
        g11 = dxdr**2 + dzdr**2
        g22 = dxdt**2 + dzdt**2
        g12 = dxdr*dxdt + dzdr*dzdt
        g33 = x0**2
        xj = (dzdr*dxdt-dxdr*dzdt)**2  #!gg=g11*g22-g12*g12
        gg = xj
        g = xj*g33
        g2v1 = 1.0/np.sqrt(g22)
        g2jq = np.sqrt(g22/xj)
        g3v  = 1.0/np.sqrt(g33)
        #--------------------------------------
        #  magnetic field
        #--------------------------------------
        bt= self.b_tor*(self.r0/self.rm)/x0
        bp=g2jq*g3v*xmy
        b=np.sqrt(bp*bp+bt*bt)
        si=bp/b
        co=bt/b
        return bt, bp, si