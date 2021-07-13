# How to use Skynet
This document contains step-by-step instructions for using **Skynet**, the automatic sleep-state classification system made for Chung-Weber Lab.


### Table of Contents
1. Preparing the conda environment
2. Installing PyTorch
3. Downloading the necesary scripts
4. Running Skynet
5. Upgraded annotation interface


### 1. Preparing the conda environment
If you have been using functions in *sleepy.py*, you probably already have a conda environment ready for use. If you do, you can skip this part and move on to **2. Installing PyTorch**.

If you don't have a conda environment or want to make a new conda environment just for Skynet, you can follow the steps here:

First, open the Anaconda Prompt.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/prompt.png)

The following code will create a new conda environment titled 'skynet38' using python 3.8:
```
conda create -n skynet38 python=3.8
```
You can use a different name for the environment and a different version of python. However, I recommend using python 3.8 as Skynet was made using python 3.8.

Once you enter the code to create a new environment, you will be asked if you would like to install several basic packages. Type 'y' and press 'Enter'.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/1b.png)

Once the new environment is created, you can activate that environment with the following code:
```
conda activate skynet38
```
You can tell that skynet38 (the new environment) has been activated by the fact that the text in the parantheses has changed from 'base' to 'skynet38'.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/1c.png)

Now that you have created a new conda environment, it is time to install all the packages/libraries used by *sleepy.py* and *sleep_annotation_qt.py*.

You can install any package with the command 'conda install' or 'pip install' followed by the name of the package. For example, to install 'seaborn', a library useful for data visualization, you can run:
```
conda install seaborn
```
While it is recommended to install using the 'conda install' command, some packages can only be installed using 'pip install'.

Here is a list of the packages you need to install using 'pip install':
* pyqt5
* sklearn

Here is a list of the packages you need to install using 'conda install':
* pyqtgraph
* scipy
* h5py
* matplotlib
* h5py
* seaborn

Your conda environment is now ready! All that is left to use **Skynet** is to install PyTorch, an open source machine learning library.


### 2. Installing PyTorch

First, activate the conda environment that has all the necessary packages installed. Then, go to the 'Get Started' page on the PyTorch website using [this link](https://pytorch.org/get-started/locally/).

There, you will find a small widget that outputs the command to run based on your selections. Most of the computers at the lab are *Windows* computers with *cpu*s only.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/2a.png)

Copy the command and run it in your conda environment.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/2b.png)

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/2d.png)

You have now successfully installed PyTorch!



### 3.
