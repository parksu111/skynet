# How to use Skynet
This document contains step-by-step instructions for using **Skynet**, the automatic sleep-state classification system made for Chung-Weber Lab.


## Table of Contents
- [Preparing the conda environment](#preparing-the-conda-environment)
- [Installing PyTorch](#installing-pytorch)
- [Downloading the necessary files](#downloading-the-necessary-files)
- [Running **Skynet**](#running-skynet)
- [Upgraded annotation interface](#upgraded-annotation-interface)
- [Current issues with **Skynet**](#current-issues-with-skynet)


## Preparing the conda environment
If you have been using functions in *sleepy.py*, you probably already have a conda environment ready for use. If you do, you can skip this part and move on to [**Installing PyTorch**](#installing-pytorch).

If you don't have a conda environment or want to make a new conda environment just for **Skynet**, you can follow the steps here:

First, open the Anaconda Prompt.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/prompt.png)

The following command will create a new conda environment titled 'skynet38' using python 3.8:
```
conda create -n skynet38 python=3.8
```
You can use a different name for the environment and a different version of python. However, I recommend using python 3.8 as **Skynet** was made using python 3.8.

Once you enter the code to create a new environment, you will be asked if you would like to install several basic packages. Type 'y' and press 'Enter'.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/1b.png)

Once the new environment is created, you can activate that environment with the following command:
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

Your conda environment is now ready! Now it is time to install PyTorch, an open source machine learning library.


## Installing PyTorch

First, activate the conda environment that has all the necessary packages installed. Then, go to the 'Get Started' page on the PyTorch website using [this link](https://pytorch.org/get-started/locally/).

There, you will find a small widget that outputs the command to run based on your selections. Most of the computers at the lab are *Windows* computers with *cpu*s only.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/2a.png)

Copy the command and run it in your conda environment.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/2b.png)

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/2d.png)

You have now successfully installed PyTorch!



## Downloading the necessary files

There are 3 files that need to be downloaded:
* skynetv1_1.pkl - A pickle file containing the trained neural network weights and biases
* skynetv1_1.py - The script for the **Skynet** system
* saqt.py - Updated version of the sleep annotation interface

These files can be found in the Penn Box repository [here](https://upenn.box.com/s/qps4kajyvd8p75k12f0i0bunw5sdmr78). All the files besides *skynet_v1_1.pkl* can also be downloaded off this very github repository. 

Download these 3 files and place them in the same folder as *sleepy.py*. Typically, this folder is the *PySleep* folder.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/3a.png)


## Running Skynet

To run **Skynet**, you must first create 2 folders. The first folder will contain the recrodings you want to classify and the second folder will contain the output of **Skynet**. For simplicity, in the example below, I named the two folders *infile* and *outfile* and placed them both in the *Desktop*.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/4a.png)

Place the recordings you wish to classify into the *infile* folder.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/4b.png)


Next, open the *skynetv1_1.py* script using a text editor or IDE like *Sublime Text* or *Spyder*. On lines 18 and 19, change the paths to match the *infile* and *outfile* folders you created. Don't forget to save the script.

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/4c.png)

Now, open the anaconda prompt and activate the environment you created in **part 1**.
The following command will run **Skynet**:
```
python skynet_v1_1.py
```
![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/4d.png)

**Skynet** is now running. It will begin by making images of each 2.5 s bin of EEG data and then proceed to classify the images. Once it is done classifying, it will output 2 files in the *outfile* folder for each recording:
* *remidx_*
* *remprob_*

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/4e.png)

Place these two files in the corresponding recording folder. 

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/4f.png)

Congratulations! You have now succesfully used the **Skynet** system. 

**Skynet** will also automatically delete all the images it made. (It moves the files to trash bin. It does NOT empty the trash bin).

Unfortunately, **Skynet** is not yet perfect and requires a small bit of manual annotation afterwards. Below, I will go over the new functions of the [upgraded annotation interface](#upgraded-annotation-interface) and some of the [current issues with Skynet](#current-issues-with-skynet).


## Upgraded annotation interface

Below is a screenshot of the new sleep annotation interface. You can run it the same way you run the old interface but the script has a new name:
```
python saqt.py
```

![alt text](https://github.com/parksu92/sleep-state-classification/blob/main/images/5a.png)

As you can see, there is a new color-coded hypnogram labelled 'Prob' above the original Brainstate hypnogram. The portions in red correspond to the 8% of bins for which **Skynet** is most unsure of the state. The portions in black correspond to bins in which there are improper state transitions (e.g. Wake --> REM or REM --> NREM). When using **Skynet**, it is advised to go through the black portions and manually annotate those bins.

Some of you are already using a version of the annotation interface that has more colors for different states. This version of the annotation interface also contains those extra states:
* Key = 't'; Dark Blue; '6' in *remidx_*
* Key = 'b'; Yellow; '7' in *remidx_*
* Key = 'c'; Light green; '4' in *remidx_*
* Key = 'v'; Red; '5' in *remidx_*

Besides these changes, everything is the same as the older *sleep_annotation_qt.py* interface.


## Current issues with Skynet

As of 07/14/2021, Skynet achieves an overall accuracy of around 94%.

When examining the results, there are 2 common problems (that I noticed. There could be more):
* Often, the REM periods end with NREM before going into Wake. These are caught by the system and are displayed in black in the 'prob' hypnogram of *saqt.py*
* There are short blocks (1 or 2 bins) of NREM in the middle of long Wake blocks. When looking just at the EEG and EMG, these bins look like NREM. However, we usually annotate it as Wake. These are not caught by the system yet.

Please report any issues you notice to me via Slack or email (parksu@alumni.upenn.edu).

I will continue to upgrade Skynet to try and increase the accuracy.

Thank you!

