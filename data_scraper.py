from langchain_community.document_loaders import SeleniumURLLoader

from github import Github

def linkedin_data(url):
    loader = SeleniumURLLoader(urls=[url])
    data = loader.load()
    return data[0]

def github_data(username):
    client = Github()

    user = client.get_user(username)
    repos = user.get_repos()

    repo_info = []
    for repo in repos:
        repo_info.append({
            "name": repo.name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "labels": repo.get_labels(),
            "issues": repo.get_issues(state="all"),
            "contents": repo.get_contents(""),

        })

    return repo_info

if __name__ == "__main__":
    # result = linkedin_data("https://www.linkedin.com/in/yingliu-data/")
    # print(result)

    from github import Github

    client = Github()

    user = client.get_user("sophia172")
    repos = user.get_repos()

    repo_info = []
    for repo in repos:
        repo_info.append({
            "name": repo.name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "labels": repo.get_labels(),
            "issues": repo.get_issues(state="all"),
            "contents": repo.get_contents(""),

        })
    import pickle
    with open("github_info.pkl", "wb") as file:
        pickle.dump(repo_info, file)
    print(repo_info)