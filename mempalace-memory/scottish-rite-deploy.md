# Scottish Rite Deploy Rule

## ALWAYS Deploy to BOTH Targets

### 1. Zo Computer — `https://scottish-rite-jaknyfe.zocomputer.io/`
1. `cd /home/workspace/scottish-rite && bun run build`
2. `cp dist/index.html dist/assets/* /home/workspace/scottish-rite-site/`
3. `cd /home/workspace/scottish-rite-site && git add . && git commit -m "Update [description]" && git push origin master`

### 2. NoesisGroup — `https://noesisgroup.com/scottish_rite/`
1. Fetch: `sshpass -p '@EUjgrN9fkr5li8$' scp noesisuser@65.38.97.58:/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html /tmp/noesisgroup-scottish-rite.html`
2. Edit the HTML locally
3. Upload: `sshpass -p '@EUjgrN9fkr5li8$' scp /tmp/noesisgroup-scottish-rite.html noesisuser@65.38.97.58:/var/www/vhosts/noesisgroup.com/httpdocs/scottish_rite/index.html`

NEVER serve directly from Vite dist/ output for noesisgroup.com — different codebase (React 18 + Babel standalone, single HTML file).
