# pynbody histograms
import pynbody
import pylab
from utils import load_snapshot, format_snapshot
from config import SNAPSHOT_PATH

def make_histogram(main_halo):
    """
    Calculate the metalicity relative to solar (Fe/H) by requesting the 'feh' array. 
    Can access certain main_halo arrays to make visualisations easier.
    """
    pylab.hist(main_halo.s['feh'], bins=100, histtype='step', color='r', label='Stars', range=(-3.0, 0.2), density=True)
    pylab.hist(main_halo.g['feh'], bins=100, histtype='step', color='b', label='Gas', range=(-3.0, 0.2), density=True)
    pylab.xlabel("[Fe/H]")
    pylab.legend()
    pylab.show()


def make_2d_hist(main_halo):
    """
    The 2d histogram for the main halo.
    """
    pynbody.plot.hist2d(main_halo.s['feh'], main_halo.s['ofe'], logscale=True, cmap='Blues', nbins=128,
                    x_range=(-3, 0.2), y_range=(-1, 1))
    pylab.xlabel("[Fe/H]")
    pylab.ylabel("[O/Fe]")
    pylab.show()
    
def make_dt_hist(main_halo):
    """
    Histogram of density-temperature relations using 'rho_T()'
    """
    pynbody.plot.gas.rho_T(main_halo.g)
    pylab.show()


def main():
    print("\nTo see a visualization, select one of the following:\n")
    print("1. Metallicity relative to solar histogram")
    print("2. 2d histogram")
    print("3. Density temperature relation histogram\n")
    
    cmd = input("Enter number (1-3) or q to quit: ")
    if cmd == "q":
        return

    snapshot, halos, main_halo = load_snapshot(SNAPSHOT_PATH)
    format_snapshot(snapshot, main_halo) # center snapshot and convert to physical units

    if cmd == "1":
        make_histogram(main_halo)
        main()
    elif cmd == "2":
        make_2d_hist(main_halo)
        main()
    elif cmd == "3":
        make_dt_hist(main_halo)
        main()
    else:
        print("Invalid option. Please enter a number between 1 and 3.")
        main()

if __name__ == "__main__":
    main()
