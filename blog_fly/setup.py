from setuptools import setup, find_packages


setup(
    name='blog_fly',
    version='0.1',
    description='Blog System base on Django',
    author='the_fly',
    author_email='xiaofei10011314@163.com',
    url='https://github.com/xiaofei1015/blog_fly/tree/wlf.dev',
    license='MIT',
    packages=find_packages('blog_fly'),
    package_dir={'': 'blog_fly'},
    package_data={'': [
        'theme/*/*/*/*',
    ]},
    install_requires=[
        'Django~=1.11', 'xadmin==0.6.1', 'pyMySQL==0.9.3', 'pillow==5.1.0',
        'djangorestframework==3.8.2', 'django-debug-toolbar==1.9.1', 'djdt_flamegraph==0.2.12',
        'django-redis==4.9.0', 'redis==2.10.6', 'mistune==0.8.3',
    ],
    extra_require={
        'ipython': ['ipython==6.2.1']
    },
    script=[
        'blog_fly/manage.py'
    ],
    entry_point={
        'console_scripts':[
            'blog_fly_manage = manage.main',
        ]
    },
    classifiers = [
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)