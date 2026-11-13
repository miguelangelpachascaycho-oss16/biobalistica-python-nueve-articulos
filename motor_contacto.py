"""Herramientas comunes para aprender impacto normal y comparar soluciones.

No contiene parámetros de células reales. m=v0=1 son escalas adimensionales.
q es indentación del blanco: el proyectil se supone rígido y el blanco fijo.
"""
import math
import numpy as np
from scipy.optimize import brentq


COLUMNAS = ['s','q','v','fuerza','energia_elastica','energia_disipada',
            'energia_total','q_referencia','v_referencia','delta_sobre_R']
RADIO_RELATIVO = 30.0  # R/L; la misma escala geométrica para los nueve casos.


def paso_rk4(derivadas, tiempo, estado, paso):
    """Un paso de Runge-Kutta de orden 4; retorna un nuevo vector de estado."""
    k1 = np.asarray(derivadas(tiempo, estado))
    k2 = np.asarray(derivadas(tiempo + paso/2, estado + paso*k1/2))
    k3 = np.asarray(derivadas(tiempo + paso/2, estado + paso*k2/2))
    k4 = np.asarray(derivadas(tiempo + paso, estado + paso*k3))
    return estado + paso*(k1 + 2*k2 + 2*k3 + k4)/6


def integrar_contacto(fuerza, k=1., n=1.5, paso=0.002, criterio='fuerza'):
    """Integra (q,v,Wdis) y localiza la separación por bisección del último paso.

    fuerza(q,v) devuelve la reacción firmada del contacto, positiva al comprimir.
    Se integra Wdis'=(F-k*q**n)*v para comprobar el balance de energía.
    criterio='fuerza' corta al anularse la fuerza al descargar; 'q' reproduce
    el antiguo criterio q=0 únicamente para comparaciones explícitas.
    """
    if paso <= 0 or k <= 0 or n <= 0:
        raise ValueError('Se requieren paso, rigidez y exponente positivos')
    def derivadas(t, y):
        q, v, _ = y
        f = fuerza(max(q,0.), v)
        elastica = k*max(q,0.)**n
        return np.array([v, -f, (f-elastica)*v])
    def evento(y):
        if y[1] >= 0:
            return 1.0  # Aún carga: no confundir el contacto inicial con separación.
        return y[0] if criterio == 'q' else fuerza(max(y[0],0.),y[1])
    t=0.;y=np.array([0.,1.,0.]);filas=[(t,*y)]
    for _ in range(int(30/paso)):
        siguiente=paso_rk4(derivadas,t,y,paso)
        if evento(siguiente) <= 0:
            inferior,superior=0.,paso
            for _ in range(38):
                mitad=(inferior+superior)/2
                candidato=paso_rk4(derivadas,t,y,mitad)
                if evento(candidato)>0: inferior=mitad
                else: superior=mitad
            dt=(inferior+superior)/2
            y=paso_rk4(derivadas,t,y,dt);y[0]=max(y[0],0.)
            filas.append((t+dt,*y))
            break
        t+=paso;y=siguiente;filas.append((t,*y))
    else:
        raise RuntimeError('No hubo separación antes de s=30')
    d=np.asarray(filas);t,q,v,dis=d.T
    f=np.array([fuerza(qi,vi) for qi,vi in zip(q,v)])
    u=k*np.maximum(q,0.)**(n+1)/(n+1)
    energia=.5*v*v+u+dis
    return np.column_stack((t,q,v,f,u,dis,energia,
                            np.full(len(t),np.nan),np.full(len(t),np.nan),q/RADIO_RELATIVO))


def primitiva_velocidad(v, beta=0., eta=0.):
    """H(v)=integral de v/g(v); admite Hertz, Hunt-Crossley y ley exponencial.

    g=1, 1+beta*v o exp(eta*v). Las series evitan cancelación cerca de v=0.
    """
    if eta:
        z=eta*v
        if abs(z)<1e-3:
            return sum((-eta)**j*v**(j+2)/((j+2)*math.factorial(j)) for j in range(7))
        return (-np.expm1(-z)-z*np.exp(-z))/eta**2
    if beta:
        z=beta*v
        if abs(z)<1e-3:
            return sum((-beta)**j*v**(j+2)/(j+2) for j in range(7))
        return (z-np.log1p(z))/beta**2
    return .5*v*v


def cuadratura_contacto(k=1., n=1.5, beta=0., eta=0., puntos=801):
    """Solución semianalítica independiente de RK4, desde la primera integral.

    H(v)+k*q**(n+1)/(n+1)=H(1). Se resuelven ambas ramas de v(q) por
    raíces escalares y se integra dt=dq/v con cambio trigonométrico regular.
    'Semianalítica' señala que raíces y cuadratura se evalúan numéricamente.
    """
    h0=primitiva_velocidad(1.,beta,eta)
    qmax=((n+1)*h0/k)**(1/(n+1))
    minimo=-min(1.,(1-1e-10)/beta) if beta else -1.
    if beta or eta:
        rebote=brentq(lambda v:primitiva_velocidad(v,beta,eta)-h0,minimo,-1e-12,xtol=1e-13)
    else: rebote=-1.
    angulo=np.linspace(0,np.pi/2,puntos)
    carga=qmax*np.sin(angulo);descarga=qmax*np.cos(angulo)
    def velocidad(q, rama):
        resto=max(0.,h0-k*q**(n+1)/(n+1))
        if resto<1e-14: return 0.
        if h0-resto<1e-13: return 1. if rama>0 else rebote
        if not (beta or eta): return rama*np.sqrt(2*resto)
        limites=(0.,1.) if rama>0 else (rebote,0.)
        return brentq(lambda v:primitiva_velocidad(v,beta,eta)-resto,*limites,xtol=1e-12)
    vc=np.array([velocidad(q,1) for q in carga])
    vd=np.array([velocidad(q,-1) for q in descarga])
    tc=np.empty(puntos);td=np.empty(puntos)
    tc[:-1]=qmax*np.cos(angulo[:-1])/vc[:-1]
    td[1:]=qmax*np.sin(angulo[1:])/(-vd[1:])
    # Límite de dq/v en el máximo: v²≈2 F(qmax)*(qmax-q).
    tc[-1]=td[0]=np.sqrt(qmax/(k*qmax**n))
    def acumular(valores):
        return np.r_[0.,np.cumsum((valores[:-1]+valores[1:])*np.diff(angulo)/2)]
    sc=acumular(tc);sd=acumular(td)+sc[-1]
    curva=np.column_stack((np.r_[sc,sd[1:]],np.r_[carga,descarga[1:]],np.r_[vc,vd[1:]]))
    return curva,{'qmax':float(qmax),'restitucion':float(-rebote),'tiempo_contacto':float(sd[-1])}


def referencia_lineal(tiempos, zeta):
    """Solución temporal cerrada y separación sin atracción para 0<zeta<1."""
    if not 0<zeta<1: raise ValueError('Este ejemplo requiere amortiguamiento subcrítico')
    omega=np.sqrt(1-zeta*zeta)
    t=np.asarray(tiempos)
    q=np.exp(-zeta*t)*np.sin(omega*t)/omega
    v=np.exp(-zeta*t)*(np.cos(omega*t)-zeta*np.sin(omega*t)/omega)
    tf=np.arctan2(2*zeta*omega,2*zeta*zeta-1)/omega
    vf=np.exp(-zeta*tf)*(np.cos(omega*tf)-zeta*np.sin(omega*tf)/omega)
    return q,v,{'tiempo_contacto':float(tf),'restitucion':float(-vf)}


def serie_inicial(tiempos, d, limite=.12):
    """Serie asintótica docente de la ley viscoelástica; NaN fuera del dominio."""
    t=np.asarray(tiempos)
    q=t-(4*d/15)*t**2.5-(4/35)*t**3.5
    v=1-(2*d/3)*t**1.5-(2/5)*t**2.5
    q[t>limite]=np.nan;v[t>limite]=np.nan
    return q,v


def completar_referencia(datos, tipo, valor, k=1., beta=0., eta=0.):
    """Añade referencia analítica o semianalítica sin volver a integrar la ODE."""
    d=datos.copy();extras={}
    if tipo in ('hertz','hc','ln','flores','exponencial'):
        curva,extras=cuadratura_contacto(k=k,beta=beta,eta=eta)
        d[:,7]=np.interp(d[:,0],curva[:,0],curva[:,1])
        d[:,8]=np.interp(d[:,0],curva[:,0],curva[:,2])
        extras['tipo_referencia']='Primera integral exacta; tiempo por cuadratura (semianalítica)'
    elif tipo=='lineal':
        d[:,7],d[:,8],extras=referencia_lineal(d[:,0],valor)
        extras['tipo_referencia']='Solución temporal cerrada'
    else:
        d[:,7],d[:,8]=serie_inicial(d[:,0],valor)
        extras['tipo_referencia']='Serie temporal de tiempo corto, s<=0.12; no exacta'
        extras['limite_serie']=.12
        _,limite=cuadratura_contacto()
        extras['limite_elastico_sin_disipacion']=limite
        if tipo=='serie':
            extras['e_serie_orden1']=1-1.15344*valor
            extras['e_serie_orden2']=1-1.15344*valor+.79826*valor*valor
    return d,extras


def metricas_contacto(datos, referencia):
    """Mide indentación, fuerza, tiempo, restitución, energía y error de referencia."""
    finitos=np.isfinite(datos[:,7])
    salida={'indentacion_maxima_L':float(datos[:,1].max()),
            'indentacion_maxima_sobre_R':float(datos[:,9].max()),
            'fuerza_maxima':float(datos[:,3].max()),
            'tiempo_contacto':float(datos[-1,0]),'restitucion':float(-datos[-1,2]),
            'indentacion_al_separar_L':float(datos[-1,1]),
            'energia_disipada':float(datos[-1,5]),
            'energia_elastica_al_separar':float(datos[-1,4]),
            'error_balance_energia':float(np.max(abs(datos[:,6]-.5))),
            'error_q_referencia':float(np.max(abs(datos[finitos,1]-datos[finitos,7]))),
            'referencia':referencia}
    return salida


def perfil_blanco(radios, indentacion, radio_esfera=RADIO_RELATIVO):
    """Reconstrucción superficial cuasiestática de Hertz, w(0)=indentación.

    Es una hipótesis espacial común, no un FEM ni una solución de ondas o daño.
    En leyes disipativas solo q(t) se resuelve dinámicamente; se adopta este
    perfil para visualizarlo. No se infieren tensiones ni deformación unitaria.
    """
    r=np.abs(np.asarray(radios));q=max(float(indentacion),0.)
    if q==0: return np.zeros_like(r)
    a=np.sqrt(radio_esfera*q)
    w=np.empty_like(r)
    dentro=r<=a;w[dentro]=q-r[dentro]**2/(2*radio_esfera)
    fuera=~dentro;rf=r[fuera]
    w[fuera]=((2*a*a-rf*rf)*np.arcsin(a/rf)+a*np.sqrt(rf*rf-a*a))/(np.pi*radio_esfera)
    return w
