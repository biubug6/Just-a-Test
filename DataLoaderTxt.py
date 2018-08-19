import torch.utils.data as data
import numpy as np
import os
from collenctions import defaultdict
import torch
from torchvision.datasets.folder import default_loader

class RandomIdentitySampler(data.sampler.Sampler):
    def __init__(self, data_source, num_instances = 1):
        self.data_source = data_source
        self.num_instances  = num_instances
        self.index_dic = defaultdict(list)
        for index, (_, pid, _) in enumerate(data_source.infos):
            self.index_dic[pid].append(index)
        self.pids  = list(self_dic.keys())
        self.num_samples = len(self.pids)
        
    def __len__(self):
        return self.num_samples * self.num_instances
        
    def __iter__(self):
        indices = torch.randperm(self.num_samples)
        ret = []
        for i in indices:
            pid = self.pid[i]
            t = self.index_dic[pid]
            if len(t) >= self.num_instances:
                t = np.random.choice(t, size = self.num_instances, replace = False)
            else:
                t = np.random.choice(t, size = self.num_instances, replace = True)
            ret.extend(t)
        return iter(ret)
   
class TxtDataset(data.Dataset):
    """
    Args:
        root (string): Root directory path.
        txtfile (string): each line includes (indentity, cam_id, filename) in txtfile
        transform (callable, optional)
    """
    def __init__(self, root, txtfile, transform = None, test = False, loader = default_loader):
        self.root  = root
        self.transform = transform
        self.loader = loader
        self.test = test
        
        self.infos, self.classes, self.ids, self.cams = self.readtxt(txtfile)
        
    def readtxt(self, txtfile):
        """
        return tuples that contain full image path, label, CamID
        """
        with open(txtfile) as file:
            lines = file.readlines()
            
        infos = []
        for line in lines:
            infos.append( np.array(line.split()))
            
        IDs = np.array(infos)[:, 0]
        CamIDs = np.array(infos)[:, 1]
        unique_ID = np.sort(np.unique(IDs))
        class_to_idx = {unique_ID[i]: i for i in range(len(unique_ID))}

        images = []
        for info in infos:
            if self.test:
                label = info[0]
            else:
                label = class_to_ids[info[0]]
            fullpath = os.path.join(self.root, info[2])
            cam = info[1]
            item = (fullpath, label, cam)
            images.append(item)
        return images, unique_ID, IDs, CamIDs
    
    def __getitem__(self, index):
        path, label, cam = self.infos[index]
        img = self.loader(path)
        if self.transform is not None:
            img = self.transform(img)
        return img, label, int(cam)
    
    def __len__(self):
        return len(self.infos)
                
