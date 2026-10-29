"""Future local-only analysis. Public demo and synthetic events cannot enter it.

Usage: python3 analysis/analyze.py /restricted/roster.jsonl --release /reviewed/release.json
The committed release intentionally refuses observed analysis.
"""
import argparse
import hashlib
import json
import math
import re
import statistics
from pathlib import Path

FIELDS = {'schema_version','data_kind','environment','protocol_version','stimulus_version',
          'participant_id','consent','eligible','clarity','atmosphere','answers','confidence',
          'booking_intention','appeal','technical_failure'}
CELLS = [(0,0),(0,1),(1,0),(1,1)]

def validate_release(release):
    if release.get('status') != 'approved_for_collection':
        raise ValueError('Observed analysis blocked: release is not approved for collection.')
    if not release.get('stimulus_version') or any(x in release['stimulus_version'].lower() for x in ['demo','diagram','test','synthetic']):
        raise ValueError('A frozen non-demo stimulus version is required.')
    hashes=release.get('stimulus_sha256',[])
    if len(hashes)!=24 or not all(isinstance(h,str) and re.fullmatch('[a-f0-9]{64}',h) for h in hashes):
        raise ValueError('Release requires 24 stimulus file hashes (six per cell).')
    items=release.get('items',[])
    if len(items)!=6: raise ValueError('Release must contain six frozen items.')
    for item in items:
        options=item.get('options',[])
        if len(set(options))!=len(options) or len(options)<3 or item.get('correct') not in options or 'cannot_tell' not in options or item['correct']=='cannot_tell':
            raise ValueError('Invalid item options or scoring key.')
    return release

def nullable_int(value, low, high, name):
    if value is not None and (type(value) is not int or not low<=value<=high):
        raise ValueError('Invalid '+name)

def validate_record(row, release):
    if set(row)!=FIELDS: raise ValueError('Input fields differ from the restricted schema; unknown fields are prohibited.')
    if row['data_kind']!='observed' or row['environment']!='approved_study':
        raise ValueError('Demo/test/synthetic data are prohibited in observed analysis.')
    if type(row['schema_version']) is not int or row['schema_version']!=1: raise ValueError('Unsupported schema')
    if row['protocol_version']!=release['protocol_version'] or row['stimulus_version']!=release['stimulus_version']:
        raise ValueError('Release mismatch')
    if not isinstance(row['participant_id'],str) or not re.fullmatch('[A-Za-z0-9_-]{8,80}',row['participant_id']):
        raise ValueError('Invalid nonidentifying participant ID')
    if row['consent'] is not True or row['eligible'] is not True: raise ValueError('Consent and eligibility must precede assignment')
    for x in ['clarity','atmosphere']:
        if type(row[x]) is not int or row[x] not in [0,1]: raise ValueError('Invalid condition')
    if type(row['technical_failure']) is not bool: raise ValueError('Invalid technical_failure')
    if not isinstance(row['answers'],list) or len(row['answers'])!=6: raise ValueError('Six answers, including explicit nulls, required')
    for answer,item in zip(row['answers'],release['items']):
        if answer is not None and answer not in item['options']: raise ValueError('Invalid item response')
    nullable_int(row['confidence'],0,100,'confidence')
    for x in ['booking_intention','appeal']: nullable_int(row[x],1,7,x)
    return row

def score(row, release):
    if any(a is None for a in row['answers']): return None
    return sum(a==q['correct'] for a,q in zip(row['answers'],release['items']))

def summarize(rows, release):
    if not rows: raise ValueError('No randomized roster records supplied')
    seen=set()
    groups={cell:[] for cell in CELLS}
    for r in rows:
        validate_record(r,release)
        if r['participant_id'] in seen: raise ValueError('Duplicate participant ID; resolve against audit trail')
        seen.add(r['participant_id']); groups[(r['clarity'],r['atmosphere'])].append(r)
    counts={}
    for cell,records in groups.items():
        values=[v for v in (score(r,release) for r in records) if v is not None]
        counts[str(cell)]={'assigned_n':len(records),'complete_n':len(values),'missing_n':len(records)-len(values),
                           'technical_failure_n':sum(r['technical_failure'] for r in records),
                           'mean_correct':statistics.mean(values) if values else None}
    def cellmean(cell,fill=None):
        values=[score(r,release) for r in groups[cell]]
        if fill is not None: values=[fill if v is None else v for v in values]
        else: values=[v for v in values if v is not None]
        return statistics.mean(values) if values else None
    means=[cellmean(c) for c in CELLS]
    result={'status':'observed_complete_outcome_estimate_with_missingness_limits',
            'roster_n':len(rows),'cells':counts,'primary_units':'correct items out of six',
            'clarity_difference':None,'ci95_normal':None,'p_two_sided_normal':None,
            'full_roster_bounds':None,'inference':'insufficient cell outcomes',
            'secondary_status':'Descriptive/exploratory; no revenue or actual-booking endpoint'}
    if all(v is not None for v in means):
        result['clarity_difference']=(means[2]+means[3]-means[0]-means[1])/2
        values=[[score(r,release) for r in groups[c] if score(r,release) is not None] for c in CELLS]
        if min(map(len,values))>=2:
            se=math.sqrt(sum(statistics.variance(v)/len(v) for v in values)/4)
            diff=result['clarity_difference']
            result['standard_error']=se
            result['ci95_normal']=[diff-1.95996398454*se,diff+1.95996398454*se]
            result['p_two_sided_normal']=math.erfc(abs(diff/se)/math.sqrt(2)) if se else None
            result['inference']='asymptotic primary inference' if min(map(len,values))>=50 else 'diagnostic only: at least one cell has fewer than 50 complete outcomes'
    if all(groups[c] for c in CELLS):
        low=(cellmean((1,0),0)+cellmean((1,1),0)-cellmean((0,0),6)-cellmean((0,1),6))/2
        high=(cellmean((1,0),6)+cellmean((1,1),6)-cellmean((0,0),0)-cellmean((0,1),0))/2
        result['full_roster_bounds']=[low,high]
    result['secondary_by_cell']={str(c):{k:{'n':len(v:=[r[k] for r in groups[c] if r[k] is not None]),'mean':statistics.mean(v) if v else None} for k in ['confidence','booking_intention','appeal']} for c in CELLS}
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--release',type=Path,default=Path(__file__).resolve().parents[1]/'data/release.json')
    args=parser.parse_args()
    try:
        release=validate_release(json.loads(args.release.read_text()))
        raw=args.input.read_bytes()
        rows=[json.loads(line) for line in raw.decode().splitlines() if line.strip()]
        output=summarize(rows,release)
        output['input_sha256']=hashlib.sha256(raw).hexdigest()
        output['release_sha256']=hashlib.sha256(args.release.read_bytes()).hexdigest()
        print(json.dumps(output,indent=2))
    except (ValueError,KeyError,TypeError) as error:
        parser.exit(2,'Analysis refused: '+str(error)+'\n')

if __name__=='__main__': main()
