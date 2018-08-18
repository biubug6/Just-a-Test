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
