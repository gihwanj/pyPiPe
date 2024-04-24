print('Loading Correlation! Version 1')

def CorrelationFunction(filepath, dt, Nf):
    import Correlation
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from numpy.polynomial import polynomial as poly
    """
    Load data from the given file and compute the correlation function, then plot it.

    Parameters:
        filepath (str): Path to the data file.
        dt (float): Time interval.
        Nf (int): Maximum time interval for correlation function calculation.

    Returns:
        ndarray: Correlation function values.
    """
    # Load data
    # f = 's24-06643/sse/_Project_/test1/sv_petraj_Block=50_T2.npy'
    D = np.load(filepath)
    Plj = D[0, :, 0]

    # Create time array
    t = np.arange(len(Plj)) * dt

    # Calculate correlation function
    C = []
    for t in range(1, Nf):
        ct = (Plj[:-t] * Plj[t:]).mean() - Plj.mean()**2
        C.append(ct)
    C = np.array(C)

    # Plot the graph
    plt.semilogy(range(1, Nf), C / np.max(C))
    plt.xlabel(r'$Time$', fontsize=16)
    plt.ylabel('C(t,t\')', fontsize=16)
    plt.title('Correlation Function', fontsize=16)
    plt.show()

    # Return correlation function values
    return C
