'''
Script + instructions to define own custom datatset
please see https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
for more details
'''
import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from torch.datasets import make_dataset, find_classes
from skimage import io

'''
torch.utils.data.Dataset is an abstract class representing a dataset. Your custom dataset should inherit Dataset and override the following methods:

__len__ so that len(dataset) returns the size of the dataset.
__getitem__ to support the indexing such that dataset[i] can be used to get iith sample.

In most cases before one can begin training an ML model on a dataset you first need to decide the train/dev/test splits. 
This processs often takes up a considerable amount of time and it is important that the sets are balanced and bias in the
datasets have been addressed. It is key that the test set must be engineered in a manner to act a a truly unseen dataset.
On creation of the train/val/test splits it is common practive to 
'''
class CustomDataset(Dataset):
    
    def __init__(self, csv_file, root_dir, transform=None, split='train'):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
            split (string): {train,val,test}
        """
        self.split = split
        self.dataset = pd.read_csv(csv_file)
        self.dataset = self.dataset[self.dataset['split'] == self.split]
        self.root_dir = root_dir
        self.transform = transform

    def __getitem_(self, idx):
        img_name = os.path.join(self.root_dir,
                                self.dataset_paths['paths'].iloc[idx]) 
        image = io.imread(img_name)
        label = self.dataset['label'].iloc[idx]
        if self.transform:
            x = self.transform(image)
        return {'y': label, 'x': x}

    def __len__(self):
        return len(self.dataset_path)