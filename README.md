# ASL-Controlled-Smart-Home-Environment

ASL (American Sign Language) controlled smart home environment, specifically catered to those with hearing and/or verbal impairments.
Program will be operable on a Raspberry Pi.

# Download

We decided to use Anaconda because it could run pyTorch (for Windows users) and opencv (for macOS users) a lot more easily than other ways. You will need to download
Anaconda in order to run our program. You will then need to download the opencv and pyTorch packages. You must then clone our repo from GitHub

## Anaconda

Go to the Ancadonda website: "https://www.anaconda.com/distribution/"
When you click the download button it should bring you down so that you can choose your system type Windows | macOS | Linux
Then go under Python 3.7 and choose which installer version you need (32x vs 64x)
Go through the Anaconda Installer and choose all default options 

## Anaconda Packages

For Windows Users:
Go to the start or seach bar on your Desktop and search for "Anaconda Prompt (Anaconda3)"

Creating a Testing Enironment within Anaconda:
```bash
conda create --name ASL
y
conda activate ASL
```
On the side of your prompt it should now say (ASL) instead of (base) on the new line

Downloading Packages:
```bash
conda install opencv
y
conda install pytorch torchvision cpuonly -c pytorch
y
```

## Repository
You can either download a zip file or clone our repo via terminal. If you wish to download the zip go to: "https://github.com/CrimsonSword01/ASL-Controlled-Smart-Home-Environment"

Cloning the Github:
```bash
git clone https://github.com/mjp1997/ASL-Controlled-Smart-Home-Environment.git
cd ASL-Controlled-Smart-Home-Environment/
```

# Initial Camera and Log
Controls for Camera:
Press `Esc` to exit the camera (Note: If `Esc` doesn't work then press `Ctrl + C`)

Controls for Log:
Press `C` to Clear the Log

# Developers

Paul Durham, Allison Dorsett, Joseph Proctor, Benjamin Jinkerson, Mitchell Perez, Omnia Awad

