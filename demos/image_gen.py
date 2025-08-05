# pynbody snapshot visualisations
import pynbody
import pylab
from utils import load_snapshot, format_snapshot
from config import SNAPSHOT_PATH

def visualise_gas_density(main_halo):
    """
    Generate a density interpolation of gas for the main halo (central galaxy).
    """
    pynbody.plot.image(main_halo.gas, width=100, cmap='Blues')
    pylab.show()


def visualise_dark_matter_distribution(snapshot):
    """
    Generate a dark matter distribution visualisation for the entire snapshot.
    """
    pynbody.plot.image(snapshot.d[pynbody.filt.Sphere('10 Mpc')],
                    width='10 Mpc', units = 'Msol kpc^-2',
                    cmap='Greys')
    pylab.show()


def visualise_sideon_gas(main_halo):
    """
    Generate a side-on view of the gas distribution for the main halo.
    """
    pynbody.analysis.sideon(main_halo)
    pynbody.plot.image(main_halo.gas, width=100, cmap='Blues')
    pylab.show()


def main():
    print("\nTo see a visualization, select one of the following:\n")
    print("1. Central galaxy density interpolation of gas")
    print("2. Dark matter distribution of entire snapshot")
    print("3. Side-on view of gas distribution\n")
    
    cmd = input("Enter number (1-3) or q to quit: ")
    if cmd == "q":
        return

    snapshot, halos, main_halo = load_snapshot(SNAPSHOT_PATH)
    format_snapshot(snapshot, main_halo) # center snapshot and convert to physical units

    if cmd == "1":
        visualise_gas_density(main_halo)
        main()
    elif cmd == "2":
        visualise_dark_matter_distribution(snapshot)
        main()
    elif cmd == "3":
        visualise_sideon_gas(main_halo)
        main()
    else:
        print("Invalid option. Please enter a number between 1 and 3.")
        main()

if __name__ == "__main__":
    main()
