# loading snapshot using pynbody and getting some data
from utils import load_snapshot
from config import SNAPSHOT_PATH

def get_snapshot_data(s, h, main_halo):
    
    # log the min_halo's data to console
    print('\nngas = %e, ndark = %e, nstar = %e\n'%(len(main_halo.gas),len(main_halo.dark),len(main_halo.star)))
    # ...also works with the whole snapshot
    # can abbreviate .gas .dark .star -> .g .d .s
    print('Whole snapshot ngas = %e, ndark = %e, nstar = %e\n'%(len(s.g),len(s.d),len(s.s)))
    # ...and any other halo
    print('Halo 5 ngas = %e, ndark = %e, nstar = %e\n'%(len(h[5].gas),len(h[5].dark),len(h[5].star)))

def main():
    # Load the snapshot
    snapshot, halos, main_halo = load_snapshot(SNAPSHOT_PATH) # check utils for how to load a snapshot
    get_snapshot_data(snapshot, halos, main_halo)

if __name__ == "__main__":
    main()