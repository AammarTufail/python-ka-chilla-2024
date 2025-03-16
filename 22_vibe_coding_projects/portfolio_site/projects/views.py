import requests
from django.shortcuts import render

def project_list(request):
    github_url = "https://api.github.com/users/AammarTufail/repos"
    try:
        response = requests.get(github_url)
        response.raise_for_status()
        repos = response.json()
    except requests.exceptions.RequestException:
        repos = []

    # Custom short descriptions mapping (repository name -> custom description)
    custom_descriptions = {
        "Project1": "This project uses machine learning to optimize industrial processes.",
        "Project2": "A data visualization tool for industrial KPIs and performance metrics.",
        "Project3": "An automated report generator that integrates various industrial data sources."
    }
    
    # Custom images mapping (repository name -> image URL)
    custom_images = {
        "Project1": "https://github.com/AammarTufail/python-ka-chilla-2024/raw/main/00_resources/posters/02_poster.png",
        "Project2": "https://link.to/project2_image.png",
        "Project3": "https://link.to/project3_image.png"
    }

    for repo in repos:
        # Override description if custom description exists
        if repo['name'] in custom_descriptions:
            repo['description'] = custom_descriptions[repo['name']]
        # Use custom image if provided; otherwise, use GitHub's open_graph_image_url (if available)
        if repo['name'] in custom_images:
            repo['image_url'] = custom_images[repo['name']]
        else:
            repo['image_url'] = repo.get('open_graph_image_url', '')

    return render(request, 'projects/project_list.html', {'repos': repos})
