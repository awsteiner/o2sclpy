#  ───────────────────────────────────────────────────────────────────
#    Compute the Gelman-Rubin diagnostic for multiple chains with 
#    varying lengths, considering burn-in.
#    - chains: A dictionary where keys are chain names and values 
#    are NumPy arrays of chain samples.
#    - burn_in_fraction: 10% for now at line 47.
#    Returns:
#    - R_hat: The Gelman-Rubin diagnostic statistic for specified 
#    parameter (e.g. log_wgt).
#  ───────────────────────────────────────────────────────────────────

import o2sclpy
import numpy as np
import h5py

def gelman_rubin_diag(file_path,param):

    # Load the table using O2SCL
    o2scl_settings=o2sclpy.lib_settings_class()
    hf=o2sclpy.hdf_file()
    hf.open(file_path)
    tab=o2sclpy.table()
    name=b''
    o2sclpy.hdf_input_table(hf,tab,name)
    hf.close()

    chains = {}

    # Construct the chains for individual walkers
    with h5py.File(file_path, 'r') as f:
        n_walk=f['n_walk'][0]
        for i in range(0,n_walk):
            chain_i = []
            for j in range(0,tab.get_nlines()):
                if tab['walker'][j]==i:
                    for k in range(0,int(tab['mult'][j])):
                        chain_i.append(tab[param][j])
            chains[f'chain_{i}'] = np.array(chain_i)
    
    chain_keys = list(chains.keys())
    num_chains = len(chain_keys)
    
    # Burn-in period about 10% of the chain length
    burn_in = {}
    for key in chain_keys:
        length = len(chains[key])
        burn_in[key] = int(length * 0.1)
    
    # Find the maximum length of chains after burn-in
    max_len = max(len(chains[key]) - burn_in[key] for key in chain_keys)
    
    # Pad chains to have the same length with NaNs
    padded_chains = np.full((num_chains, max_len), np.nan)
    for i, key in enumerate(chain_keys):
        length = len(chains[key])
        start_index = burn_in[key]
        if length > burn_in[key]:
            padded_chains[i, :length - start_index] = chains[key][start_index:]
    
    # Compute within-chain variance (ignoring NaNs)
    within_chain_var = np.nanvar(padded_chains, axis=1, ddof=1)
    
    # Compute the mean of within-chain variances across chains
    mean_within_chain_var = np.nanmean(within_chain_var)
    
    # Compute the between-chain variance
    mean_samples = np.nanmean(padded_chains, axis=1)
    overall_mean = np.nanmean(mean_samples)
    between_chain_var = np.nanvar(mean_samples)
    
    # Estimate of the total variance
    num_samples_per_chain = np.nanmean(np.sum(~np.isnan(padded_chains), axis=1))
    var_est = ((num_samples_per_chain - 1) / num_samples_per_chain) * mean_within_chain_var + (1 / num_samples_per_chain) * between_chain_var
    
    # Gelman-Rubin diagnostic
    R_hat = np.sqrt(var_est / mean_within_chain_var)
    
    # Print results
    print("Gelman-Rubin diagnostic statistic (R-hat) for file:",file_path," parameter: ",param)
    print(R_hat)

    return R_hat
