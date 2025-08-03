# Create and plot custom density profiles for a snapshot
import pynbody
import pylab
from utils import load_snapshot, format_snapshot

def create_density_profile(main_halo):
    """
    Create density profiles for the star, dark matter and gas families.
    """
    star_profile = pynbody.analysis.Profile(main_halo.s, min=0.2, max=50, # min max refer to radii
                                        type='log', nbins=50, ndim=3) # num of bins & dimensionality
    dm_profile = pynbody.analysis.Profile(main_halo.d, min=0.2, max=50,
                                      type='log', nbins=50, ndim=3)
    gas_profile = pynbody.analysis.Profile(main_halo.g, min=0.2, max=50,
                                       type='log', nbins=50, ndim=3)
    
    return star_profile, dm_profile, gas_profile

def plot_profiles(star_profile, dm_profile, gas_profile):
    """
    Plot the created profiles
    """
    pylab.plot(star_profile['rbins'], star_profile['density'], 'r', label='Stars')
    pylab.plot(dm_profile['rbins'], dm_profile['density'], 'k', label='Dark Matter')
    pylab.plot(gas_profile['rbins'], gas_profile['density'], 'b', label='Gas')
    pylab.loglog()
    pylab.xlabel('r [kpc]')
    pylab.ylabel(r'$\rho$ [M$_\odot$/kpc$^3$]')
    pylab.legend()
    pylab.show()

def main():
    print("\nCreate a density profile\n")
    
    snapshot_path = '../testdata/gasoline_ahf/g15784.lr.01024.gz'
    snapshot, halos, main_halo = load_snapshot(snapshot_path)
    format_snapshot(snapshot, main_halo)
    star, dm, gas = create_density_profile(main_halo)
    plot_profiles(star, dm, gas)
    
    
if __name__ == "__main__":
    main()