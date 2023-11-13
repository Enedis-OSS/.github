import requests
import os

org_name = os.environ.get("ORG_NAME")

def get_org_repos(org_name):
    url = f"https://api.github.com/orgs/{org_name}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        return repos
    else:
        return None

def generate_markdown_list(repos):
    if repos:
        markdown_list = "## Dépôts de l'Organisation\n\n"
        
        for repo in repos:
            markdown_list += f"- [{repo['name']}]({repo['html_url']})\n"
        return markdown_list
    else:
        return "Erreur lors de la récupération des dépôts de l'organisation."

def update_readme():
    repos = get_org_repos(org_name)
    markdown_list = generate_markdown_list(repos)

    # Mettez à jour le fichier README.md à une certaine position (ici, après une balise spécifique)
    readme_path = os.path.join(os.getcwd(), "README.md")
    with open(readme_path, "r") as readme_file:
        content = readme_file.read()

    # Recherchez une balise spécifique dans le fichier README (par exemple, <!-- ORG_REPOS -->)
    insertion_point = content.find("<!-- ORG_REPOS -->")

    if insertion_point != -1:
        updated_content = content[:insertion_point + len("<!-- ORG_REPOS -->")] + "\n" + markdown_list + content[insertion_point + len("<!-- ORG_REPOS -->"):]
        
        with open(readme_path, "w") as readme_file:
            readme_file.write(updated_content)

if __name__ == "__main__":
    update_readme()