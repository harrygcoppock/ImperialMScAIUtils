'''
Script + instructions to define own custom dataset
please see https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
for more details
'''
import os
import random
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from skimage import io
import pandas as pd

'''
torch.utils.data.Dataset is an abstract class representing a dataset. Your custom dataset should inherit Dataset and override the following methods:

__len__ so that len(dataset) returns the size of the dataset.
__getitem__ to support the indexing such that dataset[i] can be used to get ith sample.

In most cases before one can begin training an ML model on a dataset you first need to decide the train/dev/test splits. 
This processs often takes up a considerable amount of time and it is important that the sets are balanced and bias in the
datasets have been addressed. It is key that the test set is engineered in a manner to act as a truly unseen dataset.
On creation of the train/val/test splits it is common practive to create a csv file detailing file paths + split designation. 
In the case of CW1 it is a slightly different situation, that the training and validation sets have been provided to you as 
as single dataset and it is down to you to create the validation set. By default this is just a random split. When one 
wants to create a different transform for train and validation however one runs into complications as it is 
the dataset class which handles transforms in the torch api. Best practice would be to create a csv/txt detailing each
sample's path and whether it is part of train/val/test. Then create a custom dataset with varying transforms/preprocessing.

Below is an example of how you might do this.
'''
class CustomDataset(Dataset):
    
    def __init__(self, csv_file, root_dir, transform=None, split='train'):
        """
        Args:
            csv_file (string): Path to the csv file with meta data + splits
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
            split (string): {train,val,test}
        """
        self.split = split
        self.dataset = pd.read_csv(csv_file)
        # so now only instances in split can be called.
        self.dataset = self.dataset[self.dataset['split'] == self.split]
        self.root_dir = root_dir
        self.transform = transform

    def __getitem_(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.dataset['paths'].iloc[idx]) 
        image = io.imread(img_name)
        label = self.dataset['label'].iloc[idx]
        if self.transform:
            x = self.transform(image)
        return {'y': label, 'x': x}

    def __len__(self):
        return len(self.dataset_path)

'''
We can also define custom transforms. For this we create new transforms as callable
classes - they just need the __call__ method. You can also add an __init__ if you want
to apply some additional set up processing
'''

class BareBonesTransform(object):
    """
    basic buidling block for a custom transform
    p: place holder for an arg that you may want to pass to the contructor (not needed)
    """

    def __init__(self, p):
        assert isinstance(p, float)
        self.p = p

    def __call__(self, x):

        assert isinstance(x, torch.Tensor)
        if random.uniform(0,1) < self.p:
            # do something to x some of the time
            x = x**2

        return x


def main(df, path):
    '''
    path (str): path to dataset directory
    '''
    train_dataset = CustomDataset(path_to_csv, path_to_datset, split='train', transform=train_transform)
    val_dataset = CustomDataset(path_to_csv, path_to_dataset, split='val', transform=test_transform)
    test_datset =CustomDataset(path_to_csv, path_to_datset, split='test', transform=test_transform)


