"""CRH06: working PR policy check over explicitly synthetic findings."""
import argparse,datetime,json,os
from pathlib import Path
ROOT=Path(__file__).parent

def scan(fixed=False,source=None):
    name='fixed_app.py' if fixed else 'proposed_app.py'
    relative=Path(source) if source else Path('fixtures')/name
    path=(ROOT/relative).resolve()
    if ROOT.resolve() not in path.parents:raise ValueError('Source must be inside this repository')
    relative=path.relative_to(ROOT.resolve()).as_posix()
    findings=json.loads((ROOT/'fixtures/advisories.json').read_text())
    for finding in findings:
        finding['file']=relative
        marker='PARSER_VERSION' if finding['kind']=='dependency' else 'DEBUG_LOGGING'
        finding['line']=next(i for i,line in enumerate(path.read_text().splitlines(),1) if marker in line)
    for line,text in enumerate(path.read_text().splitlines(),1):
        if 'DEMO_ONLY_NOT_A_REAL_CREDENTIAL' in text:
            findings.insert(0,{'id':'DEMO-SECRET-001','kind':'secret','file':relative,'line':line,
              'severity':'high','confidence':'high','reachable':True,'owner':'application-team',
              'remediation':'Remove the literal, resolve a secret reference at runtime, and rotate a real credential if one was exposed.',
              'source':'Actual fixture pattern match on a nonfunctional demonstration marker.'})
    return findings

def exception_for(finding, exceptions, today):
    for ex in exceptions:
        if ex.get('finding_id')!=finding['id']:continue
        try:expiry=datetime.date.fromisoformat(ex.get('expires',''))
        except (ValueError,TypeError):continue
        if expiry>=today and all(ex.get(k) for k in ['owner','approved_by','reason']):return ex
    return None

def decide(finding,mode,exceptions,today):
    if mode=='before':return 'BLOCK',None
    # A confirmed exposed credential must be removed; a fixture exception cannot bypass it.
    if finding['kind']=='secret':return 'BLOCK',None
    ex=exception_for(finding,exceptions,today)
    if ex:return 'TRACK',ex
    if finding['confidence']=='high' and finding['reachable'] and finding['severity'] in ['high','critical']:
        return 'BLOCK',None
    return 'WARN',None

def evaluate(mode='before',fixed=False,today=None,exceptions=None,source=None):
    today=today or datetime.date.today()
    exceptions=exceptions if exceptions is not None else json.loads((ROOT/'exceptions.json').read_text())['exceptions']
    findings=[]
    for f in scan(fixed,source):
        outcome,ex=decide(f,mode,exceptions,today)
        findings.append({**f,'outcome':outcome,'exception':ex})
    return {'lab':'CRH06 · Developer security controls','scope':'LOCAL EXECUTION · seeded synthetic advisory/heuristic data · no real credentials',
            'mode':mode,'fixed':fixed,'date':today.isoformat(),'status':'FAIL' if any(f['outcome']=='BLOCK' for f in findings) else 'PASS',
            'counts':{k:sum(f['outcome']==k for f in findings) for k in ['BLOCK','WARN','TRACK']},'findings':findings}

def main():
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['before','after'],default='after');p.add_argument('--fixed',action='store_true');p.add_argument('--enforce',action='store_true');p.add_argument('--source');p.add_argument('--date');p.add_argument('--output',default='artifacts/report.json');a=p.parse_args()
    report=evaluate(a.mode,a.fixed,datetime.date.fromisoformat(a.date) if a.date else None,source=a.source)
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
    if os.getenv('GITHUB_ACTIONS'):
        for f in report['findings']:
            level='error' if f['outcome']=='BLOCK' else 'warning' if f['outcome']=='WARN' else 'notice'
            print(f"::{level} file={f['file']},line={f['line']},title={f['id']} ({f['outcome']})::{f['remediation']} Owner: {f['owner']}")
        if os.getenv('GITHUB_STEP_SUMMARY'):
            Path(os.environ['GITHUB_STEP_SUMMARY']).write_text('# Synthetic conference policy check\n\n'+json.dumps(report['counts'])+'\n\nNo real credential, package advisory, or third-party scanner is involved.\n')
    print(json.dumps(report,indent=2));return int(a.enforce and report['status']=='FAIL')
if __name__=='__main__':raise SystemExit(main())
