from distutils.core import setup
from setuptools import find_packages

app_id = 'wechat_django'
app_name = 'wechat_django'
app_description = "Django utils."
install_requires = [
    'django-nested-inline'
]

VERSION = __import__(app_id).__version__

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]

setup(
    name=app_name,
    description=app_description,
    version=VERSION,
    author="CNICG",
    author_email="wangjiaxi@cnicg.cn",
    license='BSD License',
    platforms=['OS Independent'],
    url="https://git.cniotroot.cn/cnicg/"+app_name,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=CLASSIFIERS,
)
