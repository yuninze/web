import cProfile
import pstats

def prof(q):
    with cProfile.Profile() as p:
        q
    stats=pstats.Stats(p)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()