import torch
import torch.nn as nn
import numpy as np
torch.manual_seed(42)  
import warnings
import os

warnings.filterwarnings("ignore", message="CUDA initialization: The NVIDIA driver on your system is too old.*")
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message="User provided device_type of 'cuda', but CUDA is not available. Disabling")


#Convolutional layers adapted from https://www.nature.com/articles/s41598-022-19212-6
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv = nn.Sequential(
                            nn.Conv3d(1, 32, 7, 1, padding_mode='replicate'),
                            nn.BatchNorm3d(32),
                            nn.ReLU(),
                            nn.Conv3d(32, 64, 5, 1, padding_mode='replicate'),
                            nn.BatchNorm3d(64),
                            nn.ReLU(),
                            nn.MaxPool3d(2),
                            nn.Conv3d(64,128, 5, 1, padding_mode='replicate'),
                            nn.BatchNorm3d(128),
                            nn.ReLU(),
                            nn.MaxPool3d(2),
                            nn.Conv3d(128, 256, 3, 1, padding_mode='replicate'),
                            nn.BatchNorm3d(256),
                            nn.ReLU(),
                            nn.MaxPool3d(2),
                            nn.Conv3d(256,384, 1, 1, padding_mode='replicate'),
                            nn.ReLU(),
                            nn.AvgPool3d(3, stride=2),
                            nn.Dropout(0.3))

        self.mlp = nn.Sequential(nn.Linear(in_features=384, out_features=64),
                    nn.ReLU(),
                    nn.Linear(in_features=64, out_features=1))

    def forward(self, x):
        x=x.view(-1, 1, 64, 64, 64).to(dtype=torch.float32)
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.mlp(x)
        return x

def check_boxsize(vol):
    return vol.shape[0]

def load_data(vol_d_norm):
    vol_array = np.empty(shape=(1,64,64,64), dtype=np.float32)
    vol_array[:] = vol_d_norm 
    data_generator = torch.utils.data.DataLoader(vol_array, batch_size = 1, shuffle=False)
    return data_generator

def downsample(vol):
    boxsize = check_boxsize(vol)
    vol_ft = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(vol)))
    start = boxsize // 2 - 64 // 2
    stop = boxsize // 2 + 64 // 2
    vol_ft_d = vol_ft[start:stop, start:stop, start:stop]
    vol_d = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(vol_ft_d)))
    vol_d = vol_d.real
    vol_d*=((64/boxsize)**3)
    vol_d = vol_d.astype(np.float32)
    return vol_d

def upsample(vol): #through interpolation of maps in Fourier space; based on https://www.sciencedirect.com/science/article/pii/S001046551400335X
    boxsize = check_boxsize(vol)
    new_box_size = 64
    vol_ft = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(vol)))    
    padded_vol_ft = np.zeros((new_box_size, new_box_size, new_box_size), dtype=np.float32)
    padded_vol_ft[:vol.shape[0], :vol.shape[1], :vol.shape[2]] = vol_ft
    interpolated_density_map = np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift((padded_vol_ft))))
    interpolated_density_map = interpolated_density_map.real
    interpolated_density_map*=((64/boxsize)**3)
    return interpolated_density_map

def normalize(vol_data):
    d_upper = np.percentile(vol_data, 99.999)
    d_lower = np.percentile(vol_data, 0.001)
    vol_data = np.where(vol_data > d_upper, d_upper, vol_data)
    vol_data = np.where(vol_data < d_lower, d_lower, vol_data)
    vol_d_norm = np.where(vol_data <= 0, 0, vol_data)
    vol_d_min = np.min(vol_data[vol_data > 0])
    vol_d_max = np.max(vol_d_norm)
    vol_d_norm = (vol_d_norm - vol_d_min)/(vol_d_max - vol_d_min)
    vol_d_norm = 2*vol_d_norm - 1
    return vol_d_norm, vol_d_min, vol_d_max

device = torch.device("cuda") if torch.cuda.is_available() else torch.device('cpu')
model = CNNModel().to(device, dtype=torch.float32)
dir = os.path.dirname(os.path.abspath(__file__))
checkpoint = torch.load(os.path.join(dir, 'weights_5e6.pth'), weights_only=False, map_location = device)
model.load_state_dict(checkpoint['model_state_dict'])

def model_pred(data_generator):
    model.eval()
    pred_list = []
    with torch.no_grad():
        for (idx, x) in enumerate(data_generator):
            x = x.to(device, dtype=torch.float32)
            prediction = model(x)
            prediction = (prediction.squeeze(dim=1))
            pred_list.append(prediction.cpu().numpy())
    return pred_list

def calc_level_dev(vol_data):
    
    boxsize = check_boxsize(vol_data)
    
    if boxsize > 64:
        _, vol_min, vol_max = normalize(vol_data)
        vol_d = downsample(vol_data)
        vol_d_norm, _, _ = normalize(vol_d)
    
    elif boxsize < 64:
        _, vol_min, vol_max = normalize(vol_data)
        vol_d = upsample(vol_data)
        vol_d_norm, _, _ = normalize(vol_d)

    else:
        vol_d = vol_data
        vol_d_norm, vol_d_min, vol_d_max = normalize(vol_d)

    data_generator = load_data(vol_d_norm)
    pred_list = model_pred(data_generator)
    all_preds = np.concatenate(pred_list, axis = 0)
    int_preds = (all_preds + 1)/2
    
    if boxsize != 64:
        norm_preds = (int_preds * (vol_max - vol_min)) + vol_min
    else:
        norm_preds = (int_preds * (vol_d_max - vol_d_min)) + vol_d_min

    return norm_preds

def calc_level(session, volumes):
    volumes_list=[]
    for volume in volumes:
        m = volume.full_matrix()
        norm_preds = calc_level_dev(m)
        volume.set_parameters(surface_levels = norm_preds)
        volumes_list.append(volume)
        session.logger.info(f'predicted contour level is {norm_preds}')

        from chimerax.core.commands import run
        run(session, 'volume all step 1')
        run(session, 'volume all style surface')
        run(session, 'volume showOutlineBox false')

    return volumes_list

def register_command(session):
    from chimerax.core.commands import CmdDesc, register
    from chimerax.map import MapsArg
    desc = CmdDesc(required=[("volumes", MapsArg)], synopsis = 'Predict level')
    register('volume calc_level', desc, calc_level, logger=session.logger)

register_command(session)

