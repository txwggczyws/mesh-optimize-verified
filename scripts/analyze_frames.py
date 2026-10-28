"""Analyze raw blocks without merging temporal boundaries. Python 3.10+, stdlib only."""
import argparse
import json
import math
from pathlib import Path


def positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def percentile(values, q):
    if not values or not 0 <= q <= 1:
        raise ValueError('nonempty values and q in [0,1] required')
    data = sorted(values)
    pos = (len(data)-1)*q
    lo = int(pos)
    return data[lo] + (data[min(lo+1, len(data)-1)]-data[lo])*(pos-lo)


def summarize(blocks, threshold_ms):
    if not positive(threshold_ms) or not blocks or any(not b for b in blocks):
        raise ValueError('positive threshold and nonempty raw blocks required')
    values = [v for b in blocks for v in b]
    if not all(positive(v) for v in values):
        raise ValueError('frame_ms must contain finite positive numbers, not booleans/null/zero')
    longest = 0
    for block in blocks:
        streak = 0
        for value in block:
            streak = streak+1 if value > threshold_ms else 0
            longest = max(streak, longest)
    return dict(frames=len(values), blocks=len(blocks), mean_fps=1000*len(values)/sum(values),
                p50_ms=percentile(values,.5), p95_ms=percentile(values,.95),
                p99_ms=percentile(values,.99), max_ms=max(values),
                long_frames=sum(v > threshold_ms for v in values),
                longest_long_streak=longest, threshold_ms=threshold_ms)


def analyze(data, threshold_ms, relative_allowance, absolute_allowance_ms):
    if data.get('measurement') not in ('screen','offscreen_sync','gpu') or not data.get('environment'):
        raise ValueError('measurement must be screen/offscreen_sync/gpu; environment required')
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<0
           for v in (relative_allowance,absolute_allowance_ms)):
        raise ValueError('allowances must be finite nonnegative numbers')
    groups = {}; seen = set()
    for row in data.get('rows',[]):
        key = tuple(row[k] for k in ('session','view','arm','block'))
        if not all(isinstance(k,str) and k for k in key) or key[2] not in ('original','candidate') or key in seen:
            raise ValueError('unique nonempty session/view/arm/block strings required; arms original/candidate')
        seen.add(key)
        groups.setdefault(key[:3],[]).append(row['frame_ms'])
    if not groups:
        raise ValueError('no raw rows supplied')
    stats = {k:summarize(v,threshold_ms) for k,v in groups.items()}
    comparisons = []
    for session,view in sorted(set(k[:2] for k in groups)):
        a=stats.get((session,view,'original')); b=stats.get((session,view,'candidate'))
        limit = a['p99_ms']+max(relative_allowance*a['p99_ms'],absolute_allowance_ms) if a else None
        added_streak = (b['longest_long_streak'] >= 2 and b['longest_long_streak'] > a['longest_long_streak']) if a and b else None
        passed = b['p99_ms']<=limit and not added_streak if a and b else None
        comparisons.append(dict(session=session,view=view,original=a,candidate=b,p99_limit_ms=limit,
                                added_sustained_long_frames=added_streak,**{'pass':passed}))
    return dict(measurement=data['measurement'],environment=data['environment'],comparisons=comparisons,
                percentile_method='sorted linear interpolation at (n-1)*q; pooled only within session/view/arm',
                all_measured_comparisons_pass=all(c['pass'] is True for c in comparisons),
                full_acceptance_proven=False,
                limitation='Descriptive comparison of supplied samples only; collection validity, coverage, visual quality, and target-device acceptance need separate verification.')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--threshold-ms',type=float,required=True,help='Project-agreed long-frame threshold; no implicit FPS requirement')
    p.add_argument('--relative-allowance',type=float,required=True,help='Fraction, e.g. 0.05; user/project choice')
    p.add_argument('--absolute-allowance-ms',type=float,required=True)
    args=p.parse_args()
    try:
        if args.out.exists() or args.out.resolve()==args.input.resolve():
            raise ValueError('output must be a new file')
        result=analyze(json.loads(args.input.read_text(encoding='utf-8-sig')),args.threshold_ms,args.relative_allowance,args.absolute_allowance_ms)
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2,allow_nan=False)
        print(json.dumps(dict(output=str(args.out),all_measured_comparisons_pass=result['all_measured_comparisons_pass'])))
    except (ValueError,KeyError,TypeError,OSError) as e:p.exit(2,str(e)+'\n')


if __name__=='__main__':main()
