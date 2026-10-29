"""Draft two-arm analysis. Real collection requires reviewed files and provenance."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import statistics

FIELDS = {'schema_version','data_kind','environment','protocol_version','stimulus_version',
          'participant_id','consent','eligible','coverage','answers','confidence',
          'coverage_rating','technical_failure'}


def validate_release(release, stimulus_root):
    if release.get('status') != 'approved_for_collection':
        raise ValueError('Observed analysis blocked: release is not approved for collection.')
    if type(release.get('schema_version')) is not int or release['schema_version'] != 2 or release.get('protocol_version') != '0.2':
        raise ValueError('Unsupported release version')
    version=release.get('stimulus_version')
    if not isinstance(version,str) or not version or any(s in version.lower() for s in ['demo','diagram','test','synthetic']):
        raise ValueError('A frozen non-demo stimulus version is required')
    for field in ['review_reference','preregistration_reference']:
        if not isinstance(release.get(field),str) or not release[field].strip():
            raise ValueError('Missing '+field+'; references require human verification')
    if type(release.get('assignment_ceiling')) is not int or release['assignment_ceiling']<2:
        raise ValueError('A frozen assignment ceiling is required')
    items=release.get('items')
    if not isinstance(items,list) or len(items)!=6: raise ValueError('Six keyed items required')
    ids=[]
    for item in items:
        if not isinstance(item,dict): raise ValueError('Invalid item')
        options=item.get('options');key=item.get('correct');item_id=item.get('id')
        if not isinstance(item_id,str) or not re.fullmatch('[a-z][a-z0-9_]*',item_id): raise ValueError('Invalid item ID')
        ids.append(item_id)
        if not isinstance(options,list) or not all(isinstance(o,str) and o for o in options): raise ValueError('Options must be strings')
        if len(options)<3 or len(set(options))!=len(options) or key not in options or key=='cannot_tell' or 'cannot_tell' not in options:
            raise ValueError('Invalid options or key')
    if len(set(ids))!=6: raise ValueError('Duplicate item ID')
    ledger=release.get('answerability')
    if not isinstance(ledger,list) or len(ledger)!=6 or any(not isinstance(x,dict) for x in ledger): raise ValueError('Answerability ledger required')
    if sorted(x.get('item_id','') for x in ledger)!=sorted(ids): raise ValueError('Answerability item mismatch')
    for item in ledger:
        if item.get('broader')!='established' or item.get('narrower') not in ['established','contradicted','not_established']:
            raise ValueError('Invalid answerability; broader gallery must establish each fact')
    stimuli=release.get('stimuli')
    if not isinstance(stimuli,list) or len(stimuli)!=12: raise ValueError('Twelve mapped stimulus slots required')
    root=Path(stimulus_root).resolve();slots=set();within_arm=set();hash_paths={}
    for entry in stimuli:
        if not isinstance(entry,dict): raise ValueError('Invalid stimulus entry')
        arm=entry.get('coverage');slot=entry.get('slot');name=entry.get('path');digest=entry.get('sha256')
        if type(arm) is not int or arm not in [0,1] or type(slot) is not int or not 1<=slot<=6: raise ValueError('Invalid arm/slot')
        if (arm,slot) in slots: raise ValueError('Duplicate arm/slot')
        slots.add((arm,slot))
        if not isinstance(name,str) or not name or Path(name).is_absolute() or '..' in Path(name).parts: raise ValueError('Unsafe stimulus path')
        path=(root/name).resolve()
        if root not in path.parents or not path.is_file(): raise ValueError('Stimulus file missing/outside root')
        if (arm,path) in within_arm: raise ValueError('Repeated file within arm')
        within_arm.add((arm,path))
        if not isinstance(digest,str) or not re.fullmatch('[a-f0-9]{64}',digest) or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError('Stimulus hash mismatch')
        if digest in hash_paths and hash_paths[digest]!=path: raise ValueError('Duplicate content under different file paths')
        hash_paths[digest]=path
    return release


def nullable_int(value,lo,hi,name):
    if value is not None and (type(value) is not int or not lo<=value<=hi): raise ValueError('Invalid '+name)


def validate_record(row,release):
    if not isinstance(row,dict) or set(row)!=FIELDS: raise ValueError('Input fields differ from restricted schema')
    if row['data_kind']!='observed' or row['environment']!='approved_study': raise ValueError('Demo/test/synthetic data prohibited')
    if type(row['schema_version']) is not int or row['schema_version']!=2: raise ValueError('Unsupported schema')
    if row['protocol_version']!=release['protocol_version'] or row['stimulus_version']!=release['stimulus_version']: raise ValueError('Release mismatch')
    if not isinstance(row['participant_id'],str) or not re.fullmatch('[A-Za-z0-9_-]{8,80}',row['participant_id']): raise ValueError('Invalid study ID')
    if row['consent'] is not True or row['eligible'] is not True: raise ValueError('Consent and eligibility must precede assignment')
    if type(row['coverage']) is not int or row['coverage'] not in [0,1]: raise ValueError('Invalid coverage')
    if type(row['technical_failure']) is not bool: raise ValueError('Invalid technical failure')
    if not isinstance(row['answers'],list) or len(row['answers'])!=6: raise ValueError('Six answers including explicit nulls required')
    for answer,item in zip(row['answers'],release['items']):
        if answer is not None and (not isinstance(answer,str) or answer not in item['options']): raise ValueError('Invalid response')
    nullable_int(row['confidence'],0,100,'confidence')
    nullable_int(row['coverage_rating'],1,7,'coverage rating')
    return row


def categories(row,release):
    result=dict(correct=0,incorrect=0,cannot_tell=0,missing=0)
    for a,item in zip(row['answers'],release['items']):
        k='missing' if a is None else 'cannot_tell' if a=='cannot_tell' else 'correct' if a==item['correct'] else 'incorrect'
        result[k]+=1
    return result


def score(row,release):
    c=categories(row,release)
    return None if c['missing'] else c['correct']


def describe(values):
    return dict(n=len(values),mean=statistics.mean(values) if values else None,sd=statistics.stdev(values) if len(values)>1 else None)


def summarize(rows,release):
    if not rows: raise ValueError('No randomized roster supplied')
    if len(rows)>release['assignment_ceiling']: raise ValueError('Roster exceeds frozen assignment ceiling; review deviation')
    groups={0:[],1:[]};seen=set()
    for row in rows:
        validate_record(row,release)
        if row['participant_id'] in seen: raise ValueError('Duplicate ID; resolve against allocation audit log')
        seen.add(row['participant_id']);groups[row['coverage']].append(row)
    result=dict(status='complete_outcome_estimate_requires_missingness_assumption',roster_n=len(rows),
                units='correctly identified facts out of six',arms={},coverage_difference=None,
                standard_error=None,ci95_normal=None,p_two_sided_normal=None,
                full_roster_identification_bounds=None,bounds_are_confidence_intervals=False,
                inference='insufficient complete outcomes',secondary_status='descriptive only')
    values={}
    for arm,records in groups.items():
        values[arm]=[s for r in records if (s:=score(r,release)) is not None]
        complete=[categories(r,release) for r in records if score(r,release) is not None]
        item_counts=[]
        for j,item in enumerate(release['items']):
            c=dict(correct=0,incorrect=0,cannot_tell=0,missing=0)
            for r in records:
                a=r['answers'][j];k='missing' if a is None else 'cannot_tell' if a=='cannot_tell' else 'correct' if a==item['correct'] else 'incorrect';c[k]+=1
            item_counts.append(dict(item_id=item['id'],**c))
        result['arms'][str(arm)]=dict(assigned_n=len(records),complete_n=len(values[arm]),missing_n=len(records)-len(values[arm]),
            technical_failure_n=sum(r['technical_failure'] for r in records),correct_count=describe(values[arm]),
            complete_response_categories={k:describe([c[k] for c in complete]) for k in ['correct','incorrect','cannot_tell']},
            items=item_counts,secondary={k:describe([r[k] for r in records if r[k] is not None]) for k in ['confidence','coverage_rating']})
    if all(values.values()):
        diff=statistics.mean(values[1])-statistics.mean(values[0]);result['coverage_difference']=diff
        if min(map(len,values.values()))>=2:
            se=math.sqrt(sum(statistics.variance(v)/len(v) for v in values.values()));result['standard_error']=se
            if se==0: result['inference']='degenerate variance: descriptive contrast only; interval and p value withheld'
            else:
                result['ci95_normal']=[diff-1.95996398454*se,diff+1.95996398454*se]
                result['p_two_sided_normal']=math.erfc(abs(diff/se)/math.sqrt(2))
                result['inference']='asymptotic primary inference' if min(map(len,values.values()))>=50 else 'diagnostic only: fewer than 50 complete outcomes in an arm'
    if all(groups.values()):
        def bound(arm,upper):
            cs=[categories(r,release) for r in groups[arm]]
            return statistics.mean(c['correct']+(c['missing'] if upper else 0) for c in cs)
        result['full_roster_identification_bounds']=[bound(1,False)-bound(0,True),bound(1,True)-bound(0,False)]
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path)
    parser.add_argument('--release',type=Path,default=Path(__file__).resolve().parents[1]/'data/release.json')
    parser.add_argument('--stimulus-root',type=Path,default=Path('.'))
    args=parser.parse_args()
    try:
        release_bytes=args.release.read_bytes();release=validate_release(json.loads(release_bytes),args.stimulus_root)
        raw=args.input.read_bytes();rows=[json.loads(line) for line in raw.decode().splitlines() if line.strip()]
        result=summarize(rows,release)
        result['input_sha256']=hashlib.sha256(raw).hexdigest();result['release_sha256']=hashlib.sha256(release_bytes).hexdigest()
        print(json.dumps(result,indent=2,allow_nan=False))
    except (ValueError,KeyError,TypeError,OSError) as error:
        parser.exit(2,'Analysis refused: '+str(error)+'\n')

if __name__=='__main__':main()
