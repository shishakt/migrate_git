import requests,sys
## Get the base branch name from the Pull Request and search if the branch have RC or master or main, 
##   accordingly call the lockBranch function with the branch details.

apiProtectionLink='https://api.github.com/repos/shishakt/migrate_git/branches/master/protection'
AccessToken = sys.argv[1]
 -X PUT \
headers ={"Accept": "application/vnd.github+json","Authorization": "Bearer "+AccessToken}
lockRCBranchData  = '''{
  "required_status_checks": {
    "strict": true,
    "contexts":[]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismissal_restrictions": {
      "teams": [
        "team1"
      ]
    },
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 2,
    "bypass_pull_request_allowances": {
      "teams": [
        "admins"
      ]
    }
  },
  "restrictions": {
    "team": [ 
        "team1"
    ]
  },
  "required_linear_history": true,
  "allow_force_pushes": true,
  "allow_deletions": false,
  "block_creations": true,
  "required_conversation_resolution": true
}'''

print(lockRCBranchData)

unlockRCBranchData = '''{
  "required_status_checks": {
    "strict": true,
    "contexts":[]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismissal_restrictions": {
      "teams": [
        "team1"
      ]
    },
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "required_approving_review_count": 2,
    "bypass_pull_request_allowances": {
      "teams": [
        "admins"
      ]
    }
  },
  "restrictions": {
    "team": [ 
        "team1"
    ]
  },
  "required_linear_history": true,
  "allow_force_pushes": true,
  "allow_deletions": false,
  "block_creations": true,
  "required_conversation_resolution": true
}'''
