from __future__ import print_function, division

import torch
import os
import torch.nn as nn
import numpy as np
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import torch.nn.functional as F
import sleepy as sp
import scipy.io as so
import shutil
import time
import warnings

#Paths
ppath = r'/home/spark/Desktop/recordings'
outpath = r'/home/spark/Desktop/outfile'



def write_remprob(M, K, ppath, name) :
	"""
	rewrite_remidx(idx, states, ppath, name)
	replace the indices idx in the remidx file of recording name
	with the assignment given in states
	"""

	outfile = os.path.join(ppath, 'remprob_' + name + '.txt')

	f = open(outfile, 'w')
	s = ["%d\t%d\n" % (i,j) for (i,j) in zip(M,K)]
	f.writelines(s)
	f.close()
	
def write_remidx(M, K, ppath, name) :
	"""
	rewrite_remidx(idx, states, ppath, name)
	replace the indices idx in the remidx file of recording name
	with the assignment given in states
	"""

	outfile = os.path.join(ppath, 'remidx_' + name + '.txt')

	f = open(outfile, 'w')
	s = ["%d\t%d\n" % (i,j) for (i,j) in zip(M,K)]
	f.writelines(s)
	f.close()


class twochannelDataset(Dataset):
	def __init__(self, path_eeg1, path_emg, transform=None):
		self.data_eeg1 = datasets.ImageFolder(root=path_eeg1, transform=transform)
		self.data_emg = datasets.ImageFolder(root=path_emg, transform=transform)

	def __getitem__(self, index):
		x_eeg1, y = self.data_eeg1[index]
		x_emg, _ = self.data_emg[index]
		a = self.data_eeg1.samples[index]
		b = self.data_emg.samples[index]
		return x_eeg1, x_emg, y, a, b

	def __len__(self):
		return len(self.data_eeg1)

	def whatclass(self):
		return self.data_eeg1.classes

import torch.nn.functional as Func

class twoChannelNet(nn.Module):
	def __init__(self):
		super(twoChannelNet, self).__init__()

		eeg1_modules = list(models.resnet18().children())[:-1]
		self.model1 = nn.Sequential(*eeg1_modules)

		emg_modules = list(models.resnet18().children())[:-1]
		self.model2 = nn.Sequential(*emg_modules)

		self.fc1 = nn.Linear(1024, 100)
		self.fc2 = nn.Linear(100, 10)
		self.fc3 = nn.Linear(10, 3)

	def forward(self, eeg1, emg):
		a = self.model1(eeg1)
		b = self.model2(emg)
		x = torch.cat((a.view(a.size(0),-1), b.view(b.size(0),-1)),dim=1)
		x = Func.relu(self.fc1(x))
		x = Func.relu(self.fc2(x))
		x = self.fc3(x)
		return x



device = torch.device('cpu')
net = twoChannelNet()
net.load_state_dict(torch.load('skynet_v1_1.pkl', map_location=device))
net.eval()


recordings = os.listdir(ppath)

os.mkdir(os.path.join(ppath, 'spectogram'))

warnings.filterwarnings("ignore")
for rec in recordings:
	print('Now working on the recording ' + rec + ':')
	time.sleep(3)
	print('Making images...')
	recpath = os.path.join(ppath,'spectogram',rec)
	os.mkdir(recpath)
	eeg1path = os.path.join(recpath,'eeg1')
	emgpath = os.path.join(recpath,'emg')
	os.mkdir(eeg1path)
	os.mkdir(emgpath)
	eeg1picpath = os.path.join(eeg1path,'noclass')
	emgpicpath = os.path.join(emgpath, 'noclass')
	os.mkdir(eeg1picpath)
	os.mkdir(emgpicpath)
	M,S = sp.load_stateidx(ppath, rec)
	EEG1 = np.squeeze(so.loadmat(os.path.join(ppath, rec, 'EEG.mat'))['EEG']).astype('float')
	EMG = np.squeeze(so.loadmat(os.path.join(ppath, rec, 'EMG.mat'))['EMG']).astype('float')
	for idx,x in enumerate(M):
		if (idx>1)&(idx+2<len(M)):
			start = idx - 1
			end = idx + 2
			eeg_start = start*2500
			eeg_end = end*2500
			eeg1arrays = []
			emgarrays = []
			for substart in np.arange(eeg_start, eeg_end, 250):
				seqstart = substart-500
				seqend = substart+1000
				sup = list(range(seqstart, seqend+1))
				eeg1pow,F = sp.power_spectrum(EEG1[sup],1000,1/1000)
				emgpow,F = sp.power_spectrum(EMG[sup],1000,1/1000)
				ifreq = np.where((F>=0)&(F<=20))
				subeeg1 = eeg1pow[ifreq]
				subemg = emgpow[ifreq]
				eeg1arrays.append(subeeg1)
				emgarrays.append(subemg)
			totEEG1 = np.stack(eeg1arrays, axis=1)
			totEMG = np.stack(emgarrays, axis=1)

			fig1 = plt.figure(figsize=(3.0,2.1),dpi=100)
			plt.subplots_adjust(top=1,bottom=0,right=1,left=0,hspace=0,wspace=0)
			plt.imshow(totEEG1,cmap='hot',interpolation='nearest',origin='lower')
			plt.gca().set_axis_off()
			plt.margins(0,0)
			plt.axis('off')
			plt.gca().xaxis.set_major_locator(plt.NullLocator())
			plt.gca().yaxis.set_major_locator(plt.NullLocator())
			fig1.savefig(os.path.join(eeg1picpath,str(idx)+'.png'))

			fig2 = plt.figure(figsize=(3.0,2.1),dpi=100)
			plt.subplots_adjust(top=1,bottom=0,right=1,left=0,hspace=0,wspace=0)
			plt.imshow(totEMG,cmap='hot',interpolation='nearest',origin='lower')
			plt.gca().set_axis_off()
			plt.margins(0,0)
			plt.axis('off')
			plt.gca().xaxis.set_major_locator(plt.NullLocator())
			plt.gca().yaxis.set_major_locator(plt.NullLocator())
			fig2.savefig(os.path.join(emgpicpath,str(idx)+'.png'))

			plt.close('all')

		if idx == int(len(M)/25):
			print('25%')
		if idx == int(len(M)/25)*2:
			print('50%')
		if idx == int(len(M)/25)*3:
			print('75%')                             

	print('Images have been made.')
	time.sleep(3)
	print('Now classifying the images...')
	print('...')

	#load recording
	M,S = sp.load_stateidx(ppath, rec)
	Mnew = np.repeat(-1, len(M))
	#paths for input images
	inpath1 = os.path.join(ppath, 'spectogram', rec, 'eeg1')
	inpath2 = os.path.join(ppath, 'spectogram', rec, 'emg')
	#prepare dataset and dataloader
	imset = twochannelDataset(inpath1, inpath2, transforms.Compose([transforms.ToTensor()]))
	im_loader = torch.utils.data.DataLoader(imset, batch_size=1, shuffle=False)
	#Classify images
	score_diffs = []
	inds = []
	for i, (im1, im2, lbl, n1, n2) in enumerate(im_loader, 0):
		output = net(im1, im2)
		_,pred = torch.max(output.data, 1)
		outlist = output.data.tolist()[0]
		largest = max(outlist)
		outlist.remove(max(outlist))
		sec_largest = max(outlist)
		score_diffs.append(largest - sec_largest)
		ind = int((n1[0][0].split('/')[-1]).split('.')[0])
		Mnew[ind] = pred
		inds.append(ind)
	#Convert prediction integers to states
	resM = []
	for x in Mnew:
		if x==0:
			resM.append('N')
		elif x==1:
			resM.append('R')
		else:
			resM.append('W')
	#Lowest certainty
	score_diffs = np.array(score_diffs)
	perc8 = np.percentile(score_diffs, 8)
	low8 = np.where(score_diffs < perc8)[0] 
	#Bad state transitions
	badstate_idx = []
	ind1 = 0
	while ind1 < len(resM)-1:
		curr = resM[ind1]
		nxt = resM[ind1+1]
		if (curr == 'W')&(nxt == 'R'):
			badstate_idx.append(ind1)
			badstate_idx.append(ind1+1)
		if (curr == 'R')&(nxt == 'N'):
			badstate_idx.append(ind1)
			badstate_idx.append(ind1+1)
		ind1+=1
	# Make stateprob list
	remprob = np.repeat(0, len(M))
	for i in range(len(M)):
		if i in low8:
			remprob[i] = 1
		if i in badstate_idx:
			remprob[i] = 2
	# Make remidx list
	nnres = []
	for x in Mnew:
		if x==0:#nrem
			nnres.append(3)
		elif x==1:
			nnres.append(1)
		else:
			nnres.append(2)   
	kdiffs = list(np.repeat(0,len(M)))
	write_remprob(remprob, kdiffs, outpath, rec)
	write_remidx(nnres, kdiffs, outpath, rec)
	print('...')
	print('Images have been classified.')
	time.sleep(3)
	print('Deleting images for ' + rec)
	shutil.rmtree(os.path.join(ppath, 'spectogram', rec))
	print('Images have been deleted.')
	print(' ')

print('All recordings have been classified.')
print(' ')
print('Thank you for using SKYNET')




