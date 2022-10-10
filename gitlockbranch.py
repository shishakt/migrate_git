import requests,sys,json
## Get the base branch name from the Pull Request and search if the branch have RC or master or main, 
##   accordingly call the lockBranch function with the branch details.
# HEAD and BASE branch, get only BASE branch and update the protection rule

ORG_NAME = 'shishakt' #sys.argv[1]
REPO_NAME = 'migrate_git' # accept from cli arguments sys.argv[2]
ACESSTOKEN = sys.argv[1] # accept from cli arguments sys.argv[3]
SWITCH = sys.argv[4]
if SWITCH == 'LOCK':
    BRANCH_NAME = sys.argv[5]
elif SWITCH == 'UNLOCK':
    prNumber = sys.argv[5]
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

#print(lockRCBranchData)

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
def getBaseBranch(prNumber):
    apiPullRequestLink = 'https://api.github.com/repos/'+ORG_NAME + '/' + REPO_NAME+ '/pulls/'
    response = requests.get(apiPullRequestLink+prNumber,headers=headers)
    if response.status_code == 200:
        responseContent = response.content.decode('utf-8')
        jsonResponse = json.loads(responseContent)
        print("Base Branch is ", jsonResponse['base']['ref'])
        return jsonResponse['base']['ref']

def updateProtectionRule():
    apiProtectionLink = 'https://api.github.com/repos/'+ORG_NAME + '/' + REPO_NAME + '/branches/' + BRANCH_NAME + '/protection'
    if SWITCH == 'LOCK':
        response = requests.put(apiProtectionLink,headers=headers,data=lockRCBranchData)
        if response.status_code == 200:
            print("Locked Branch: ", BRANCH_NAME)
    elif SWITCH == 'UNLOCK':
        response = requests.put(apiProtectionLink,headers=headers,data=unlockRCBranchData)
        if response.status_code == 200:
            print("Unlocked Branch: ", BRANCH_NAME)

if __name__ == '__main__':
    try:
        if SWITCH == 'UNLOCK':
            BRANCH_NAME = getBaseBranch(prNumber)
            updateProtectionRule()
        elif SWITCH == 'LOCK':
            updateProtectionRule()
    except Exception as error:
        print("Error Occurred ",str(error))