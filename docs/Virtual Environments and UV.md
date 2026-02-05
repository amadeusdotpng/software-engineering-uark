# What is a Virtual Environment?
[Virtual environments](https://codefinity.com/courses/v2/aa507197-48a5-468a-be93-fbdfa15bb987/a1b56063-ec47-4d99-9487-5cfaf0f86eb6/b6ae943d-2c78-4efa-b178-50b756f9d703?utm_source=google&utm_medium=cpc&utm_campaign=21341099672&utm_content=&utm_term=&dki=&gad_source=5&gad_campaignid=21341100386&gclid=EAIaIQobChMI1ZyYq6WykgMVXmJHAR3pRzgKEAAYASAAEgIDnPD_BwE) are enclosed development environments for Python that allow for independent runtime (allowing different versions of Python to exist on your machine) and the dynamic switching of libraries. Tl;dr: you can have multiple versions of Python with multiple different libraries with only the inconvenience of forgetting to switch!
## Why do we use them?
Lets say I have a program that is making a Pokemon Damage Calculator and for convince, I'm using they Python library [numpy](https://numpy.org). Because I'm coding for fun, I'd probably make the code in the version of Python natively installed on my machine (3.13.11 for me) and when installing numpy, I'd just go for the most recent version:
```bash
pip install numpy
```
After making the most advanced and accurate Pokemon damage calculator of all time (its so good in fact that I will be using it on the daily), I realize that I have to do a project for my Software Engineering course. After looking at the instructor's code I realize that using numpy 1.8.13 would be optimal. Now I have to undo everything:
```bash
pip uninstall numpy
pip install numpy==1.8.2
```
This is annoying. Now I can work on my assignment for a grade, but I really like playing Pokemon and I'll constantly have to switch which version of numpy I'm using. If only there was a solution. . .

Introducing a [virtual environment](https://docs.python.org/3/library/venv.html) (venv)! With this revolutionary piece of technology, we can set up an environment for running Pokemon _AND_ one for Software Engineering!
## How to set one up
1. Enter the folder you want to make your environment
```bash
cd ~/home/TheGreatestPokemonCalculatorOfAllTime
```
2. Make the virtual environment
```bash
python -m venv .
```
- **Alternatively**, you could replace the dot (.) with the path to the folder; The dot says to make the virtual environment in this folder
- To test see if the environment is created, you can run the command 
3. Run the environment
- Depending on what you're using, you're computer's OS _may_ have a preference on which script you're running (for the sake of convince, I'm going to assume you guys are running on Windows)
```bash
.\Scripts\activate
```
4. Install what you want!
- For the story line, we're going to install the most recent version of numpy
```bash
pip install numpy
```
5. Check to see what you have installed
```bash
pip list
```

Now, whenever we want to run our damage calculator, we can run this virtual environment to make sure we're using the version of numpy we want and, when we create another virtual environment for Software Engineering, we can guarantee has the proper version of numpy by using the command `pip install numpy==1.18.13`

# What is UV?
UV is a Python project manager that uses pip but runs a lot faster with a few other benefit

The main reason to use UV over basic Python venv's is speed. UV is fast, _really_ fast. It also allows for multiple packages to be installed at the same time meaning if you're working on a code base where you have to get all the packages installed initially, UV will allow for those packages to be installed in parallel as opposed to a basic venv installing packages one at a time.  

## How to set up UV venv
Sadly, UV is a bit more tedious to get initially set up than a regular venv. Please [read the docs](https://docs.astral.sh/uv/getting-started/installation/#installation-methods), but for the most part you should just need to run this command in you're Powershell terminal (again assuming Windows):
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Good news! After the initial set up, you should be able to use a lot the previous commands to make virtual environments and just prepend UV to have it do its magic:
```bash
pip install numpy
# becomes
uv pip install numpy
```

The main different commands come in creating the environment which luckily becomes a bit easier:
```bash
uv venv
```

# Commands to Use and Abuse
## Creating a virtual environment
How to create the **most basic environment** using system defaults. It will create a hidden environment in the current folder with the name ".venv" (to see this hidden folder, you have to type the command `ls -la`)
```bash
uv venv
```

To create an environment with a custom name
```bash
uv venv <your-environment-name>
```

To create a environment with a specific version of Python (in this case Python 3.8)
```bash
uv venv --python 3.8
```

## Activating a Virtual Environment
1. Enter the folder to the environment
```bash
cd path/to/environment
```

2. Run the activation script. If you chose to name you're environment something other than the default ".venv", you may need to replace that part of the command with the name of you're environment
### Windows
```bash
.venv\Scripts\activate
```
### Mac and Linux
```bash
source .venv/bin/activate
```
## Deactivating a Virtual Environment
With a running environment, run:
```bash
deactivate
```
## Seeing what you have installed
With a running environment, run:
```bash
uv pip list
```
## Installing packages
With a running environment, run:
```bash
uv pip install <package-name>
```
Equivalently, you could also run:
```bash
uv add <package-name>
```

To install multiple packages, just use spaces:
```bash
uv pip install <package-1> <package-2> <package-3>
```

For a specific version of a package, run:
```bash
uv pip install <package-name>==<version>
```

To install from a list of packages, use the command:
```bash
uv pip install -r <file-listing-packagess>
```
Ideally, this file is just a .txt

## Uninstalling packages
With a  running environment, run:
```bash
uv pip uninstall <package-name>
```

To install multiple packages, just use spaces:
```bash
uv pip uninstall <package-1> <package-2> <package-3>
```

***If you want to change version of a package, you don't need to uninstall it first. Just install the specific version you want and Python will handle the rest***

## Saving what you have installed
With a running environment, run:
```bash
uv pip freeze > <file-name>.txt
```
Common file names are requirements.txt or REQUIREMENTS.txt 

# Useful links
- [Virtual Environment Docs](https://docs.python.org/3/library/venv.html)
- [UV Docs](https://docs.astral.sh/uv/)
	- [Installation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
	- [First Steps](https://docs.astral.sh/uv/pip/environments/)
	- [Commands](https://docs.astral.sh/uv/reference/cli/#uv-auth-token)
- [W3Schools Tutorial](https://www.w3schools.com/python/python_virtualenv.asp)

*This stupid write up was made by Daniel (he's bad at spelling 💀)*
