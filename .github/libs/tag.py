import json, os 
from datetime import datetime, timezone
from collections import OrderedDict

version = os.popen('git tag -l').read().strip().split('\n')[-1]
w,x,y,z = map(int,version.strip('v').strip().split('.'))
branch = os.popen('git rev-parse --abbrev-ref HEAD').read().strip()
'''
Versioning:
w, x, y, z - 
w :: mip era
x :: structural change  | new activity_id | new spec 
y :: experiment 
z :: other | source



'''


UPDATE_REQUIRED = False

url = os.popen('git config --get remote.origin.url').read().strip()
owner,repo = url.split('/')[-2:]

store = f'.github/status_{owner}_{repo}.json'
try:
    old = json.load(open(store,'r'))
except:
    old = None
    UPDATE_REQUIRED = True


if branch == 'main':

    MIPERA = 'CMIP6Plus'
    new = OrderedDict(repo=dict(mipera=MIPERA,repo=repo,url=url),changelog={})
    comment = ''

    #  If not wcrp-cmip, do not create this. 

    files = ['activity_id','experiment_id','source_id']
    files.reverse() # do this as new activites or experiments reset the following version numbers 

    for f,vnum in zip(files,'z y x'.split()):
        repos = json.load(open(f'{MIPERA}_{f}.json'))[f]
        keys = list(repos.keys())
        new[f] = dict(counts = len(keys), keys = keys)

        if old:
            diff = set(new[f].get('keys')) - set(old.get(f,new[f]).get('keys'))
            if len(diff):
                # and old:
                locals()[vnum] += len(diff)

                    
                UPDATE_REQUIRED = True
                for i in diff:
                    comment += f'[{vnum}] version number ↑ :: {f} ({i.strip()})\n'
                
                if vnum == 'x':
                    locals()['y'] = 0 
                    locals()['z'] = 0 
                    comment += f'-- \u03B4x resets y and z values --\n'
                elif vnum == 'y':
                    locals()['z'] = 0 
                    comment += f'-- \u03B4y resets z values --\n'
    

    # Get the current UTC timestamp
    current_utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc)
    # Format the timestamp as 'YY/MM/DD HH:MM UTC'
    formatted_timestamp = current_utc_timestamp.strftime('%Y/%m/%d %H:%M UTC')


    new['repo']['version'] = f'v{w}.{x}.{y}.{z}'

    if UPDATE_REQUIRED:
        
        comment += " \n\nFor further information: [see the wiki](wikiurl)\nv{w}.{x}.{y}.{z}.\n\n"
        
        comment += f"Version Updated: {version} \u2192 {new['repo']['version']}\n\n"
        comment = comment.split('\n')
        comment.reverse()
        print('\n'.join(comment))

    new['changelog'] = dict(last_changed=formatted_timestamp,comment=comment)
        





if UPDATE_REQUIRED and branch == 'main':   
    json.dump(new,open(store,'w'),indent=4)
elif old:
    if old['repo']['version'] != new['repo']['version']:
        UPDATE_REQUIRED = True
        print('\n'.join(old['changelog']['comment']))
        new = old
        
NEWVERSION = new['repo']['version']
print(f'\n\n{NEWVERSION} :: needs update: {UPDATE_REQUIRED}')

if branch != 'main': 
    print('automations only run on main branch. You are on:', branch)
    
print(branch)


# import pprint
# pprint.pprint(new)


