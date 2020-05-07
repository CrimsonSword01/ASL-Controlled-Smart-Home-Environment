# Sign Language Integration for Smart Homes (SLISH)

SLISH will be specifically catered to those with hearing and/or verbal impairments. The SLISH system is only guaranteed to work for Windows users.


# Download

We decided to use Anaconda because it was easier to download and use PyTorch using this system. You will need to download
Anaconda in order to run our program. You will then need to download a variety of packages listed below in the Anaconda Packages section. You must then clone our repository from GitHub.

## Anaconda

Go to the Ancadonda website: "https://www.anaconda.com/distribution/"
When you click the download button the site should bring you down so that you can choose your system type: Windows | macOS | Linux
Then go under Python 3.7 and choose which installer version you need (32x vs 64x)
Go through the Anaconda Installer and choose all default options. 

## Anaconda Packages

Cick the Windows button in the bottom left corner (Windows 10 Users) and click into the search bar. Type "Anaconda Prompt (Anaconda3)" and click on it. When the prompt opens up type and follow the directions below:

Creating a Testing Enironment within Anaconda:
```bash
conda create --name ASL
y
conda activate ASL
```
On the side of your prompt it should now say (ASL) instead of (base) on the new line. Once this has been confirmed, please type each installation line individually and then press enter button from the instructions below. If at any time the console prompts you with (y/n) always type "y" and then press the enter button to continue installing the libraries below. 

Downloading Packages (Please Download Packages in the order they are in below):
```bash
conda install pytorch torchvision cpuonly -c pytorch
conda install opencv
pip install keyboard
pip install pyHS100
pip install pyparsing
pip install imutils
```

## Repository
You can either download a zip file or clone our repo via terminal. If you wish to download the zip go to: "https://github.com/CrimsonSword01/ASL-Controlled-Smart-Home-Environment"

If you wish to clone our repo you must create a folder (in whatever directory you wish; for simplification we will say the Desktop) on the Desktop. Go into the folder you created and copy the system path. Within the anaconda terminal do the instructions below (replace PASTE SYSTEM PATH YOU PREVIOUSLY COPIED with your system path):

Cloning the Github and Running it:
```bash
cd PASTE SYSTEM PATH YOU PREVIOUSLY COPIED
git clone https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment.git
cd ASL-Controlled-Smart-Home-Environment/
python main.py
```

# Model and Data Sets

The model and data sets are to large to be put onto Github. If you would like access to these files, please contact us and we can send them to you.

# How to use our system

Please refer to either the help.txt within our github or once you have the system runnning press the "Help Button" within the GUI.

# Developers

Paul Durham, Allison Dorsett, Joseph Proctor, Benjamin Jinkerson, Mitchell Perez, Omnia Awad

