print('Loading Interpolation ! Version 1')

def CSInterpolation(filepath, smp):
    import Interpolation
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import curve_fit
    from scipy.interpolate import CubicSpline
    """
    Generate hysteresis plot and diff plot based on the given data, and return interpolated values using Cubic Spline.

    Parameters:
        filepath (str): Path to the data file.
        smp (int): The number of steps we take.

    Returns:
        ndarray: Interpolated values using Cubic Spline.
    """
    # Load data
    D = np.load(filepath)

    # Extract temperature and LJ potential energy
    Drev = D[::-1]  # reverse: LowT -> HighT
    T = Drev[:, 0]
    U = Drev[:, 1]

    # Cubic Spline interpolation
    cs = CubicSpline(T, U)
    cx = np.linspace(min(T), max(T), smp)
    cy = cs(cx)
    interpolated_values = np.column_stack((cx[::-1], cy[::-1]))

    # Initialize arrays for differences
    Cp = np.diff(U) / np.diff(T)
    CpCS = np.diff(interpolated_values[:, 1]) / np.diff(interpolated_values[:, 0])  # Forward Difference
    CpBC = np.diff(interpolated_values[:, 1][::-1]) / np.diff(interpolated_values[:, 0][::-1])  # Backward Difference
    CpCD = np.zeros_like(cx)  # Initialize array for Central Difference
    for i in range(1, len(cx) - 1):
        CpCD[i] = (cy[i + 1] - cy[i - 1]) / (2 * (cx[i + 1] - cx[i]))  # Central Difference

    # Plotting
    fig, ax = plt.subplots(1, 3, figsize=(12, 6))

    # Hysteresis plot
    ax[0].plot(T, U, 'kX-', ms=5, lw=1, label='Original P.E')
    ax[0].plot(interpolated_values[:, 0], interpolated_values[:, 1], 'r--', lw=2.5, alpha=0.7, label='Cubic Spline')
    ax[0].legend(loc='lower right')
    ax[0].set_ylabel("Potential Energy")
    ax[0].set_xlabel("Temperature")

    # Diff plot
    ax[1].plot(T[:-1], Cp, 'kX-', ms=5, lw=1, label='Original P.E')
    ax[1].plot(interpolated_values[:-1, 0], CpCS, 'r--', lw=3, alpha=0.7, label='Cubic Spline (Forward Diff)')
    ax[1].plot(interpolated_values[:-1, 0][::-1], CpBC, 'g--', lw=3, alpha=0.7, label='Cubic Spline (Backward Diff)')
    ax[1].plot(cx[1:-1], CpCD[1:-1], 'b--', lw=3, alpha=0.7, label='Cubic Spline (Central Diff)')
    ax[1].legend()
    ax[1].set_ylabel("Diff")
    ax[1].set_xlabel("Temperature")
    ax[2].plot(T[:-1], Cp, 'kX-', ms=5, lw=1, label='Original P.E')
    ax[2].plot(interpolated_values[:-1, 0], CpCS, 'r--', lw=3, alpha=0.7, label='Cubic Spline (Forward Diff)')
    ax[2].plot(interpolated_values[:-1, 0][::-1], CpBC, 'g--', lw=3, alpha=0.7, label='Cubic Spline (Backward Diff)')
    ax[2].plot(cx[1:-1], CpCD[1:-1], 'b--', lw=3, alpha=0.7, label='Cubic Spline (Central Diff)')
    ax[2].legend()
    # ax[2].set_ylabel("Diff")
    ax[2].set_xlabel("Temperature")
    ax[2].set_xlim(1.1, 1.5)  # Set x-axis range for diff plot

    

    # Show plot
    # plt.show()

    # Return interpolated values and differences
    return interpolated_values, Cp, CpCS, CpBC, CpCD
