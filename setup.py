from setuptools import setup

setup(
    name='twofa',
    version='0.1',
    py_modules=['twofa'],
    packages=['twofa'],
    # install_requires=[
    #     'click',
    #     'pyotp',
    #     'pyperclip'
    # ],
    entry_points='''
        [console_scripts]
        twofa=twofa.__main__:main
    ''',
)
