'''
Script + instructions to define own custom dataset
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
In the case of CW1 it is a slightly different situation that the training and validation sets have been provided to you as 
as single dataset and it is down to you to create the validation set. By default this is just a random split. When one 
wants to create a different transform for train and validation however one runs into complications. Best practice would be
to create a csv/txt detailing each sample's path and whether it is part of train/val/test. Then create a custom dataset with
varying transforms/preprocessing.

Below is an example of how you might do this.
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


def create_validation_set(path, n):
    '''
    Args:
        path (str): path to the unzipped dataset
        n (float): frac of set to make validation
    Returns:
        splits (csv): lists file paths with corresponding split, e.g. train/val

        path              |    split
        ----------------------------------
        elephant/1234.png | train
        tiger/1234.png    | validation
        lion/1234.png     | train
    '''
    _, class_to_indx = find_classes(path)
    instances = make_dataset(path, class_to_indx) # gen list of (path_to_instance, class)
    # randomly sample n of the train set without replacement. Note this does not sample evenly from 
    # test set.
    df = pd.DataFrame(instances, columns=['path', 'split'])
    val = df.sample(frac=n, random_state=42)
    df['split'] = df[df in ]
    return df


def main(path):
    '''
    path (str): path to dataset directory
    '''
    df = create_validation_set
    train_dataset = CustomDataset(df, path, split='train', transform=train_transform)
    val_dataset = CustomDataset(df, path, split='val', transform=test_transform)
    test_datset =CustomDataset(test_df, test_path, split='test', transform=test_transform)


if __name__ == '__main__':
    train_dataset = CustomDataset(split='train')