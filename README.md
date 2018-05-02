# stock-market

GIT Setup for Github

1> Clone 
git clone https://github.com/surinder432/stock-market.git

1.2> If already present (rebase)
git pull

2> 

cd stock-market

3.1> configuration
git config --global --edit

git commit --amend --reset-author

3.2> credential cache : expiry

git config credential.helper store

# 24 hours = 24*60*60
git config --global credential.helper 'cache --timeout 86400'

3.3> Add a file (or Let git know that file must be commited again)

git add

4> Commit changes

git commit

(Uncomment modification to be committed)

5> Push changs to Remote

git push
(short for git push origin master)

Username : emailid
Password: Secret pass

5.2> Remote location : Check output of these
git remove -v


6> 
