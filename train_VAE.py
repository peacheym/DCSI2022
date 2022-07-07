#!/usr/bin/python3

import torch; torch.manual_seed(0)
import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions

import matplotlib.pyplot as plt; plt.rcParams['figure.dpi'] = 200
from dataset_functions import SynthPresetsDataset, loadDataCategorical01
from preset_builder import build_format_preset01, build_preset


device = 'cuda' if torch.cuda.is_available() else 'cpu'
 
class Decoder(nn.Module):
    def __init__(self, latent_dims):
        super(Decoder, self).__init__()
        self.linear1 = nn.Linear(latent_dims, 32)
        self.linear2 = nn.Linear(32, 82)

    def forward(self, z):
        z = F.relu(self.linear1(z))
        z = torch.sigmoid(self.linear2(z))
        return z #.reshape((-1, 1, 28, 28))    # Todo: determine the optimal data size/shape for synth data.
    

class VariationalEncoder(nn.Module):
    def __init__(self, latent_dims):
        super(VariationalEncoder, self).__init__()
        self.linear1 = nn.Linear(82, 32)
        self.linear2 = nn.Linear(32, latent_dims)
        self.linear3 = nn.Linear(32, latent_dims)

        self.N = torch.distributions.Normal(0, 1)
        self.kl = 0

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)
        x = F.relu(self.linear1(x))
        mu =  self.linear2(x)
        sigma = torch.exp(self.linear3(x))
        z = mu + sigma*self.N.sample(mu.shape)
        self.kl = (sigma**2 + mu**2 - torch.log(sigma) - 1/2).sum()
        return z
    
    
class VariationalAutoencoder(nn.Module):
    def __init__(self, latent_dims):
        super(VariationalAutoencoder, self).__init__()
        self.encoder = VariationalEncoder(latent_dims)
        self.decoder = Decoder(latent_dims)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)
    
    
    
def train(autoencoder, data, epochs=2500):
    losses = []
    opt = torch.optim.Adam(autoencoder.parameters())
    for epoch in range(epochs):
        for x, y in data:
            x = torch.flatten(x, start_dim=1) # Flatten data here -> TODO: Change when using synth data        
            x = x.to(device) # CPU
            opt.zero_grad()
            x_hat = autoencoder(x)
            loss = ((x - x_hat)**2).sum() + autoencoder.encoder.kl
            losses.append(loss.item())
            loss.backward()
            opt.step()
        print("Epoch {}: {}".format(epoch+1, loss))
        
    
    plt.figure(figsize=(10,5))
    plt.title("Training Loss")
    plt.plot(losses,label="Loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

    return autoencoder


latent_dims = 32 # TODO: Change to something better
autoencoder = VariationalAutoencoder(latent_dims).to(device) # GPU

X, y = loadDataCategorical01("amsynth_presets.csv", DROP=True)
training_data = SynthPresetsDataset(data=X, labels=y)

# Configure data loader
dataloader = torch.utils.data.DataLoader(
    training_data,
    batch_size=32,
    shuffle=True,
    drop_last=True,
)

# todo: Ensure that the data being used is normalized for the appropriate activation function in vae.

print("-- Begin Training --")

autoencoder = train(autoencoder, dataloader, 50)

std_tensor = torch.tensor([0.0 for i in range(latent_dims)])

build_format_preset01(autoencoder.decoder(std_tensor), "[TEST]\{VAE\}VAE2_preset")

for i in range(5):
    build_format_preset01(autoencoder.decoder(torch.rand_like(std_tensor)), "NEW4-VAE({})_preset".format(str(i)))