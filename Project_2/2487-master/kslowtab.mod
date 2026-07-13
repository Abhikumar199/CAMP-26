TITLE HH slow potassium channel
: Hodgkin - Huxley potassium channel with parameters fitted to
: the data from US Bhalla and JM Bower, J. Neurophysiol. 69:1948-1983 (1993)
: Replaces original FUNCTION_TABLE-based implementation with analytic TABLE

NEURON {
    SUFFIX kslowtab
    USEION k READ ek WRITE ik
    RANGE gkbar, ik
    GLOBAL ninf, kinf, ntau, ktau
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
}

PARAMETER {
    v (mV)
    dt (ms)
    gkbar= 0.120 (mho/cm2) <0,1e9>
    ek = -70 (mV)
}

STATE {
    n k
}

ASSIGNED {
    ik (mA/cm2)
    ninf
    kinf
    ntau (ms)
    ktau (ms)
}

INITIAL {
    rates(v)
    n = ninf
    k = kinf
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    ik = gkbar*n*n*k*(v - ek)
}

DERIVATIVE states {
    rates(v)
    n' = (ninf - n)/ntau
    k' = (kinf - k)/ktau
}

PROCEDURE rates(v(mV)) {
    TABLE ninf, kinf, ntau, ktau FROM -100 TO 100 WITH 200
    ninf = 1 / (1 + exp(-(v + 19)/10))
    kinf = 0.135 + 0.865 / (1 + exp((v + 14)/6.5))
    ntau = 1.9 + 10.5 * exp(-((v + 40)/38)*((v + 40)/38))
    ktau = 200
}
