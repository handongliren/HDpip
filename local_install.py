import os
import warnings

warnings.filterwarnings("ignore", message="Setuptools is replacing distutils")
warnings.filterwarnings("ignore", message="No matching packages")

from HDpip.core import pip_api

os.system("pip cache purge")
pip_api.uninstall("HDpip")

#for dep in setup.install_requires:
#    pip.install(dep)

pip_api.install("--no-build-isolation --no-index --find-links=dist HDpip")
