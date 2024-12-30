from setuptools import find_packages, setup
from typing import List

file_path = r"C:\Users\Precision 5530 4K\Documents\Personal project\Machine Learning\End_to_End_ml_project"
HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    """
    this function will return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace ("\n", "")for req in requirements]
        
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
            
    return requirements
setup(
name = 'END_TO_END_ML_PROJECT',
version = '0.0.1',
author = 'Hikmat',
author_email = 'hikmat@spaceuniverse.africa',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)