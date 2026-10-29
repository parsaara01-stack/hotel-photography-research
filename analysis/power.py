"""Planning calculations, never estimates from participant observations."""
import json
import math

def sample_size(d=0.3, loss=0.15):
    # Two-sided normal approximation; balanced clarity levels and four cells.
    per_level = math.ceil(2 * (1.95996398454 + 0.841621233573)**2 / d**2)
    complete = 4 * math.ceil(2 * per_level / 4)
    ceiling = 8 * math.ceil(complete / (1-loss) / 8)
    return dict(assumed_d=d, alpha=0.05, power=0.80, complete_n=complete,
                per_cell=complete//4, assumed_missing=loss, assignment_ceiling=ceiling,
                method='Normal approximation; independent participants; clarity main effect')

if __name__ == '__main__':
    print(json.dumps([sample_size(d) for d in (0.2,0.3,0.4)], indent=2))
