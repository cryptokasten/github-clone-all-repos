import os
import re
import requests

def prepare(s):
    return re.sub("^export ", "", s).replace('"', "").split("=")

def read_params(fn):
    with open(fn, "rt") as f:
        return dict(map(prepare, f.read().split("\n")))

def get_repos(token, org, page, per_page):
    url = "https://api.github.com/orgs/%s/repos?page=%s&per_page=%s" % (
        org, page, per_page
    )
    auth = "token %s" % token
    return requests.get(url, headers={"Authorization": auth}).json()

def get_all_repos_names(token, org):
   res = []
   page = 1
   per_page = 100
   while True:
      repos = get_repos(token, org, page, per_page)
      if not repos:
         return res
      res.extend(list(map(lambda x: x["name"], repos)))
      page += 1

def clone_or_pull(dst, org, name):
    git = "git://github.com/%s/%s.git" % (org, name)
    sh = "cd %s ; git clone %s ; cd %s ; git pull" % (dst, git, name)
    os.system(sh)

params = read_params(os.path.expanduser("~/.github"))
token = params["GITHUB_TOKEN"]
org = params["ORG"]
clone_dst = params["CLONE_DST"]

repos_names = get_all_repos_names(token, org)

for repo in repos_names:
    clone_or_pull(clone_dst, org, repo)
