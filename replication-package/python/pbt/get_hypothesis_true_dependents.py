import json
from dependent_obj import Dependent, DependentEncoder
from github import Github
from git import Repo
from removal_util import delete_folder
import os
import time

access_token = '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'

FILE_NAME  = 'candidates.json'

LOCAL_REPO_NAME = 'candidateRepository'

SNIPPET_IMPORT_GIVEN='from hypothesis import given'
SNIPPET_IMPORT='from hypothesis import'
SNIPPET_GIVEN_DECORATOR='@given'
SNIPPET_HYPOTHESIS_GIVEN_DECORATOR='@hypothesis.given'
SNIPPET_IMPORT_HYPOTHESIS_GIVEN = 'import hypothesis.given'


def get_dependents_dictionary():

    file_dependents = open(FILE_NAME, 'r')
    dependents_json = file_dependents.read() 
    return json.loads(dependents_json)   



def uses_pbt(file_content):
    return ((file_content.count(SNIPPET_IMPORT) > 0 and file_content.count(SNIPPET_GIVEN_DECORATOR) > 0) 
            or (file_content.count(SNIPPET_IMPORT_GIVEN) > 0)
            or (file_content.count(SNIPPET_IMPORT_HYPOTHESIS_GIVEN) > 0)
            or (file_content.count(SNIPPET_HYPOTHESIS_GIVEN_DECORATOR) > 0)
        ) 



def is_python_file(filename): 
    return filename.endswith('.py')


def has_pbt_file(f, filename):
    if is_python_file(filename) == True:
        print(filename)
        return True
    else:
        return False



def get_pbt_in_files(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path) and is_python_file(file_name):
            with open(file_path, encoding="utf8") as arquivo:
                file_content = arquivo.read()
                arquivo.close()
                if uses_pbt(file_content):                    
                    return file_path
        elif os.path.isdir(file_path):
            result = get_pbt_in_files(file_path)
            if result is not None:
                return result
    return None



def get_pbt_file_name(repo): 
    Repo.clone_from(repo.clone_url, LOCAL_REPO_NAME, depth=1)
    print(f'Repository {repo.name} was cloned')
    filename = get_pbt_in_files(LOCAL_REPO_NAME)
    time.sleep(3)

    delete_folder(LOCAL_REPO_NAME)
    return filename


def get_name(string):
    partes = string.split('/')
    if len(partes) < 2:
        return ""
    return '/'.join(partes[len(partes)//2:])


def get_real_path(file_path, repo_name):
    indice = file_path.find('\\')
    if indice != -1:
        novo_texto = repo_name + file_path[indice:]
        return novo_texto
    else:
        return file_path


def add_if_true_positive(dependent_candidate, true_positives_list, git_obj):

    repository_name = dependent_candidate["name"]
    name = get_name(repository_name)
    print(f'Checking repository {name}')

    repo = git_obj.get_repo(repository_name)

    pbt_file_path = get_pbt_file_name(repo)

    if pbt_file_path is not None:
        true_positives_list.append(
            Dependent(dependent_candidate["name"], dependent_candidate["stars"], get_real_path(pbt_file_path, name), repo.html_url))



def create_json_output(true_positives_list):
    json_output = json.dumps(true_positives_list, cls = DependentEncoder, indent=4)
    with open("true_positives.json", "w") as output_file:
        output_file.write(json_output)



def get_true_positives_list(dependents_list, git_obj): 
    true_positives_list = []

    for dependent in dependents_list:
        add_if_true_positive(dependent, true_positives_list, git_obj)
            
    create_json_output(true_positives_list)
    print(f'O número de repostórios que usam PBT: {len(true_positives_list)}')



def main():
    git_obj = Github(access_token)
    dependets_info = get_dependents_dictionary()
    dependents_list = dependets_info["all_public_dependent_repos"]
    get_true_positives_list(dependents_list, git_obj)
    return None


main()