from langchain_community.document_loaders import SeleniumURLLoader

def linkedin_data(url):
    loader = SeleniumURLLoader(urls=[url])
    data = loader.load()
    return data[0]

if __name__ == "__main__":
    result = linkedin_data("https://www.linkedin.com/in/yingliu-data/")
    print(result)