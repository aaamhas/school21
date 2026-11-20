import pstats

with open('pstats-cumulative.txt', 'w') as f:
    stats = pstats.Stats('profile_output.prof', stream=f)
    stats.sort_stats('cumulative')
    stats.print_stats(5)