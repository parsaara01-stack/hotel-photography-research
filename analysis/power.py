"""Illustrative two-arm planning; not an approved recruitment target."""
import json
import math

def sample_size(d=0.3,loss=0.15):
    if not math.isfinite(d) or d<=0 or not math.isfinite(loss) or not 0<=loss<1:
        raise ValueError('Require d>0 and 0<=loss<1')
    per_arm=math.ceil(2*(1.95996398454+0.841621233573)**2/d**2)
    complete=2*per_arm
    return dict(status='illustrative_not_approved',assumed_d=d,alpha=.05,power=.8,complete_n=complete,
                per_arm=per_arm,assumed_missing=loss,assignment_ceiling=2*math.ceil(complete/(1-loss)/2),
                method='Independent-groups normal approximation; broader minus narrower coverage')

if __name__=='__main__':print(json.dumps([sample_size(d) for d in (.2,.3,.4)],indent=2))
