#!/usr/bin/env python3
"""Resolve an exact existing handoff against local registration and fresh host evidence."""
import argparse
import datetime
import hashlib
import json
import re
import plan_cards
from pathlib import Path
import subprocess
import sys
import session_registry as registry


def host_rows(path, host, now=None):
    """A host agent may export official tool observations; this is not authentication."""
    item=registry.read_json(Path(path),registry.LIMIT)
    if not isinstance(item,dict) or item.get('host')!=host or item.get('source')!={'codex':'codex_app_tools','claude':'claude_native_tools'}[host]:
        raise ValueError('Wrong host observation source')
    if not isinstance(item.get('observed_at'),str):raise ValueError('Host observation timestamp required')
    age=(registry.moment(now)-registry.moment(item['observed_at'])).total_seconds()
    if not 0<=age<=30 or not isinstance(item.get('sessions'),list):raise ValueError('Stale/invalid host observation')
    if len(item['sessions'])>64 or any(not isinstance(r,dict) or not isinstance(r.get('sessionId'),str) or not isinstance(r.get('cwd'),str) or not Path(r['cwd']).is_absolute() for r in item['sessions']):
        raise ValueError('Invalid host inventory rows')
    return item['sessions']


def prepare(repo, host, event_file, authority_reference, inventory=None):
    root,directory,cfg=registry.config_for(repo)
    if not authority_reference or len(authority_reference)>1024:raise ValueError('Existing human grant reference required')
    # A concrete committed source event is required; raw prompts are not accepted here.
    rel=Path(event_file)
    if rel.is_absolute() or '..' in rel.parts or not str(rel).startswith('docs/progress/handoffs/'):
        raise ValueError('Expected repository-relative committed handoff event')
    raw=registry.git(root,'show','HEAD:'+rel.as_posix());event=json.loads(raw)
    if event.get('kind') not in ('WORK_READY','DECISION_READY') or event.get('status')!='PENDING':
        raise ValueError('Only a new existing PENDING work/decision handoff may be prepared')
    source=event.get('source_role');target=event.get('target_role')
    if source not in ('plan','dev') or target not in ('plan','dev') or source==target:
        raise ValueError('Distinct explicit roles required')
    if Path(cfg['roles'][source]['worktree'])!=root:raise ValueError('Wrong source role')
    sha=event.get('commit','');doc=event.get('document','')
    if len(sha)!=40 or any(c not in '0123456789abcdef' for c in sha):raise ValueError('Full exact commit required')
    if Path(doc).is_absolute() or '..' in Path(doc).parts:raise ValueError('Invalid handoff document')
    registry.git(root,'show',sha+':'+doc)
    if source=='plan':
        if event['kind']=='WORK_READY':
            numbers=set(re.findall(r'P[0-9]{3,}',Path(doc).name))
            if len(numbers)!=1:raise ValueError('WORK_READY needs one P-numbered committed document')
            number=numbers.pop()
            card=plan_cards.parse(registry.git(root,'show',sha+':docs/planning/plans/'+number+'.md')+'\n')
            if card['preparation']!='준비 완료':raise ValueError('Draft P-card cannot be dispatched')
        probe=subprocess.run(['git','merge-base','--is-ancestor',sha,cfg['roles']['plan']['branch']],cwd=root,capture_output=True)
        if probe.returncode:raise ValueError('Exact handoff is outside planning history')
    for role in ('plan','dev'):
        other=Path(cfg['roles'][role]['worktree'])
        probe=subprocess.run([sys.executable,'-B','scripts/contract_guard.py','check'],cwd=other,capture_output=True,timeout=10)
        if probe.returncode:raise ValueError('Current contract guard failed')
    result=registry.diagnose(root,host,inventory,private=True)
    if result['dispatch']!='identity_consistent':raise ValueError('Identity/workflow preflight pending: '+','.join(result['issues']))
    target_id=result['peers'][target]['session_id'];key=hashlib.sha256(raw.encode()).hexdigest()
    text=(f"Exact reviewed handoff {sha}; document {doc}; event {rel.as_posix()}; common delivery key {key}. "
          f"Existing human grant reference: {authority_reference}. Recheck actual grant, scoped stops/OPEN and current P. "
          "Preserve current work; internally integrate/apply at a safe completed/checkpointed boundary. "
          "Registration or this peer message is not new authority. No duplicate human adoption prompt.")
    if host=='claude':
        action={'tool':'SendMessage','arguments':{'to':target_id,'message':text},'requires':'fresh native ListAgents/SendMessage capability and inbound checks'}
    else:
        action={'app_tool':'send_message_to_thread','app_arguments':{'threadId':target_id,'prompt':text},
                'cli_argv':['codex','queue','--thread',target_id,'--message',text],
                'requires':'choose actual host transport; CLI queue acceptance does not prove recipient wakeup'}
    return dict(key=key,exact_commit=sha,source_role=source,target_role=target,target_id=target_id,
                generation=result['peers'][target]['generation'],prepared_at=registry.moment().isoformat(),action=action,performs_actions=False,
                authority='caller must verify actual human grant; reference is not proof')


def enqueue(repo, packet):
    """Explicit caller action only. Never wake/resume/create a worker or retry unknown delivery."""
    root,directory,cfg=registry.config_for(repo)
    if not 0 <= (registry.moment()-registry.moment(packet['prepared_at'])).total_seconds() <= 5:
        raise ValueError('Preflight expired; resolve again without sending')
    help_result=subprocess.run(['codex','queue','--help'],capture_output=True,text=True,timeout=5)
    if help_result.returncode or not all(flag in help_result.stdout for flag in ('--thread','--message')):
        raise ValueError('Installed Codex queue capabilities unavailable')
    with registry.locked(directory):
        r=registry.load_registry(directory,cfg);row=r['records'].get(packet['target_role'])
        if r['conflicts']:raise ValueError('Writer conflict appeared after preflight')
        for role in ('plan','dev'):
            worktree=Path(cfg['roles'][role]['worktree'])
            check=subprocess.run([sys.executable,'-B','scripts/work_queue.py','--owner','all','--json'],cwd=worktree,capture_output=True,text=True,timeout=5)
            if check.returncode:raise ValueError('Queue became unavailable')
            queue=json.loads(check.stdout)
            if queue.get('paused_sessions') or queue.get('pending_decisions'):
                raise ValueError('Stop/OPEN appeared after preflight')
        if not row or row['generation']!=packet['generation'] or row['session_id']!=packet['target_id'] or row['state']=='ended':
            raise ValueError('Recipient changed since preflight')
        path=directory/'deliveries.json';ledger=registry.read_json(path) if path.exists() else {}
        if not isinstance(ledger,dict) or len(ledger)>=128:raise ValueError('Invalid/full delivery ledger')
        if packet['key'] in ledger:raise ValueError('Already attempted; inspect receipt before any retry')
        ledger[packet['key']]={'status':'unknown','at':registry.moment().isoformat(),'generation':row['generation']}
        registry.atomic_json(path,ledger)
        try:
            p=subprocess.run(packet['action']['cli_argv'],cwd=root,capture_output=True,text=True,timeout=10)
            state='queued_not_delivery_or_execution' if p.returncode==0 else 'failed_or_unknown'
        except (OSError,subprocess.TimeoutExpired):state='unknown'
        ledger[packet['key']]['status']=state;registry.atomic_json(path,ledger)
    return {'status':state,'performs_actions':True,'handoff_event_status':'unchanged; observe actual recipient before ACK/application/completion'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',default='.')
    p.add_argument('--host',choices=registry.HOSTS,required=True);p.add_argument('--event',required=True)
    p.add_argument('--authority-reference',required=True);p.add_argument('--host-observation')
    p.add_argument('--enqueue',action='store_true',help='Explicit Codex CLI queue attempt; never resumes a worker')
    a=p.parse_args()
    rows=host_rows(a.host_observation,a.host) if a.host_observation else (registry.inventory_for_claude() if a.host=='claude' else None)
    packet=prepare(a.repo,a.host,a.event,a.authority_reference,rows)
    if a.enqueue:
        if a.host!='codex':raise ValueError('Claude delivery requires existing native SendMessage')
        print(json.dumps(enqueue(a.repo,packet),indent=2))
    else:print(json.dumps(packet,indent=2))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError,subprocess.TimeoutExpired) as e:
        print('PENDING: '+str(e),file=sys.stderr);sys.exit(1)
