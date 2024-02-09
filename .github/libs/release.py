import os


def clean():
    cmd = '''git filter-branch -f --commit-filter '
	if [ "$GIT_AUTHOR_EMAIL" = "actions@wcrp-cmip.org" ];
	then
		skip_commit "$@";
	else
		git commit-tree "$@";
	fi' HEAD
    '''
    os.popen(cmd).read()

def newrelease(owner,repo,version,content,title=''):
    print(os.popen(f'gh repo set-default {owner}/{repo}').read())
    release = f'gh release create "{version}" -n "{content}" -t "{title}"'
    print(os.popen(release).read())
