import os
import urllib.request 

 

url_dict = { ## urls need to be inserted here
    "att_txt_files":
    "att_1st_files":
    "example_netfiles":
    "attractor_transitions":
    'KO_results':
    'OE_results':
    'changed_results':
    'crpKO_intermediate_attractors':
    'crpKO_irreversible_genes':
    'crpKO_reversible_genes':
    'crpKO_irrev_results':
    'attractor_args_d':
    'gene_status_df':
    "transcription_logtpm":
    "transcription_metadata":
    "gsym_thresholds":
    "gsym_biases":
    "gsym_zero_biases":
}

path_dict = {
    "att_txt_files": "./attfiles/att_txt_files.tar.gz",
    "att_1st_files": './attfiles/1st_csv_files.tar.gz',
    "example_netfiles": './netfiles/example_netiles.tar.gz',
    "attractor_transitions":'./results/result_attr_trans.tar.gz',
    'KO_results':'./results/result_KO_twoparam.tar.gz',
    'OE_results':'./results/result_OE_twoparam.tar.gz',
    'changed_results':'./results/changed_pre_twoparam.tar.gz',
    'crpKO_intermediate_attractors':'results/crp/a1_irrgn_crp.tar.gz',
    'crpKO_irreversible_genes':'results/crp/irrev_changed_crp.tar.gz',
    'crpKO_reversible_genes':'results/crp/rev_changed_crp.tar.gz',
    'crpKO_irrev_results':'results/crp/irrgn_crpKO.tar.gz',
    'attractor_args_d':'results/crp/attractor_args_d.pkl',
    'gene_status_df':'results/crp/gene_status_df.pkl',
    "transcription_logtpm": './tmp/all_logtpm_dat.pkl',
    "transcription_metadata": './tmp/ecoli_metadata.pkl',
    "gsym_thresholds":'./tmp/gsym_thr_ser.pkl',
    "gsym_biases":'./tmp/gsym_bias_ser.pkl',
    "gsym_zero_biases":'./tmp/gsym_biasz_ser.pkl',
}

data_name_dict = {
    "att_txt_files":'attractor text files',
    "att_1st_files":'attractor 1st state files',
    "example_netfiles":'example Boolean network files',
    "attractor_transitions":'attractor transitions results',
    'KO_results':'KO perturbation results',
    'OE_results':'OE perturbation results',
    'changed_results':'changed genes results',
    'crpKO_intermediate_attractors':'Intermediate attractors reached after perturbation',
    'crpKO_irreversible_genes':'Irreversible response genes to crp KO',
    'crpKO_reversible_genes':'Reversible response genes to crp KO',
    'crpKO_irrev_results':'Irreversibility results for crp KO',
    'attractor_args_d':'Boltzmann and Hamming weights for each attractor',
    'gene_status_df':'Whether a gene is reversible, irreversible, or unchanged upon crp KO',
    "transcription_logtpm":'Log transcript-per-million data',
    "transcription_metadata":'Transcriptional metadata',
    "gsym_thresholds":'Thresholds for binarizing genes',
    "gsym_biases":'Probability of genes being expressed above threshold',
    "gsym_zero_biases":'Probability of genes being expressed above zero',
}

 

def main():
    for file_key,data_name in data_name_dict.items():
        data_path = path_dict[file_key]
        data_url = url_dict[file_key]
        urllib.request.urlretrieve(data_url, data_path)
        print(f"{data_name} data has been downloaded and saved in {data_path}")


 

if __name__ == '__main__':

    main()