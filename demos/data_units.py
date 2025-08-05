# raw data arrays and units of a snapshot.
import pynbody
from utils import load_snapshot, format_snapshot
from config import SNAPSHOT_PATH

def raw_data(snapshot):
    """
    Raw data form snapshot in physical units (position, velocity, mass) and their units.
    """
    # Access position, velocity, and mass arrays
    pos = snapshot['pos']
    vel = snapshot['vel']
    mass = snapshot['mass']

    print(f"\nPosition array (first 5 rows):\n{pos}\n")
    print(f"Velocity array (first 5 rows):\n{vel}\n")
    print(f"Mass array (first 5 rows):\n{mass}\n")
    # units
    print(f"Position units: {pos.units}")
    print(f"Velocity units: {vel.units}")
    print(f"Mass units: {mass.units}")


def convert_units(snapshot):
    """
    Unit conversions for position, velocity, and mass arrays.
    """
    # Convert position to megaparsecs (Mpc)
    pos_mpc = snapshot['pos'].in_units('Mpc')
    print(f"\nPosition array in Mpc:\n{pos_mpc}\n")

    # Convert position to comoving megaparsecs (Mpc a h^-1) (more info in docs)
    pos_comoving = snapshot['pos'].in_units('Mpc a h**-1')
    print(f"Position array in Mpc a h^-1:\n{pos_comoving}\n")

    # Convert velocity to km/s
    vel_kms = snapshot['vel'].in_units('km s^-1')
    print(f"Velocity array in km/s:\n{vel_kms}\n")

    # Convert mass to solar masses (Msol)
    mass_msol = snapshot['mass'].in_units('Msol')
    print(f"Mass array in Msol:\n{mass_msol}")


def reset_to_original_units(snapshot):
    """
    Reset the snapshot to its original units.
    """
    snapshot.original_units()
    print(f"Position array in original units:\n{snapshot['pos']}")


def main():
    print("\nTo explore data and units, select one of the following:\n")
    print("1. Raw data and units")
    print("2. Demonstrate unit conversions")
    print("3. Reset to original units\n")
    
    cmd = input("Enter number (1-3) or q to quit: ")
    if cmd == "q":
        return

    snapshot, halos, main_halo = load_snapshot(SNAPSHOT_PATH)
    format_snapshot(snapshot, main_halo)

    if cmd == "1":
        raw_data(snapshot)
        main()
    elif cmd == "2":
        convert_units(snapshot)
        main()
    elif cmd == "3":
        reset_to_original_units(snapshot) #  set to phys units on main() call
        main()
    else:
        print("Invalid option. Please enter a number between 1 and 3.")
        main()


if __name__ == "__main__":
    main()
