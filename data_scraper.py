from langchain_community.document_loaders import SeleniumURLLoader
from github import Github
from collections import defaultdict, Counter

def linkedin_data(url):
    loader = SeleniumURLLoader(urls=[url])
    data = loader.load()
    return data[0].page_content

def jb_data(url):
    loader = SeleniumURLLoader(urls=[url])
    data = loader.load()
    return data[0]



def github_data(username):
    client = Github()

    user = client.get_user(username)
    repos = user.get_repos()

    repo_info = ""
    for repo in repos:
        repo_info += f"[name: {repo.name}. "
        repo_info += f"language: {repo.language}. "
        repo_info += f"stars: {repo.stargazers_count}. "
        repo_info += f"forks: {repo.forks_count}. ]"
    return repo_info

if __name__ == "__main__":
    result = linkedin_data("https://www.linkedin.com/in/yingliu-data/")
    print(type(result))


    # result = github_data("sophia172")
    # print(result)

    # result =