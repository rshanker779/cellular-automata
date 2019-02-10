from matplotlib import pyplot as plt



def plotter( initial_function, repeated_function, n=10, generations=100, initial_seed=None):
    """Plotter using matplotlib to plot each array."""
    im = None
    out_grid = initial_function(n, initial_seed)
    for _ in range(generations):
        if im is None:
            # Plot initial data
            im = plt.imshow(out_grid, interpolation='none', vmin=0, vmax=2)
        else:
            # update
            out_grid = repeated_function(out_grid)
            im.set_data(out_grid)
        plt.draw()
        plt.pause(0.1)