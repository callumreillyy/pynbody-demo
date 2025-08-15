import pynbody

def load_snapshot(snapshot_image):
    """
    load the snapshot, an instance of SimSnap. Handles loading data 
    with various methods (e.g load). You can then get data from this snapshot.
    In this case we get the snapshot halos.
    """
    snapshot = pynbody.load(snapshot_image) # a zoom cosmological simulation.
    halos = snapshot.halos(ignore_missing_substructure=True) # the halos which makeup the snapshot (HaloCatalogue object).
    # can set ignore_missing_substructure to False to show missing substructures
    # can show available halo id's using keys()
    main_halo = halos[0] # one of the halos (the central galaxy).
    
    return snapshot, halos, main_halo

def format_snapshot(snapshot, main_halo):
    """
    High level snapshot manipulation (pnybody.analysis) is applied to the ENTIRE simulation.
    If this is not desired, pass 'move_all = False' as variable
    """
    snapshot.physical_units() # load the snapshot as physical units
    pynbody.analysis.halo.center(main_halo, move_all=True) # center halo, set move_all to false to ONLY center this halo