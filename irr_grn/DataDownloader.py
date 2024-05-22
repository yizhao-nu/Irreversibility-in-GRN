import os
import urllib.request 

 

url_dict = { ## urls need to be inserted here
    "att_txt_files": 'https://drive.google.com/u/0/uc?id=1GgWQi6b6nk8YVnPqjCbGOWLVeo1guIck&export=download',
    "att_1st_files": 'https://drive.google.com/u/0/uc?id=1PPhYO2vVDQ2bMxv6InWdgqWRnhLAlxgQ&export=download',
    "example_netfiles": 'https://drive.google.com/u/0/uc?id=1-Iu15H1HbPIQcBu8mJJcg3q_xA51qNXp&export=download',
    "attractor_transitions": 'https://drive.google.com/u/0/uc?id=1UAQTNvudVRdZh28zOadYOR9PgB-LQD5C&export=download',
    'KO_results': 'https://drive.google.com/u/0/uc?id=1QvydaQQRY3ooV3JEWaw95EGjj96nUaPQ&export=download',
    'OE_results': 'https://drive.google.com/u/0/uc?id=1U2qRFvQ7AmOC4tzpINTWSjLReSDLuNa2&export=download',
    'changed_results': 'https://drive.google.com/u/0/uc?id=11zDDcJW68tAHB4tXJzdEikkMWG_Sx_Cg&export=download',
    'crpKO_intermediate_attractors': 'https://drive.google.com/u/0/uc?id=1kEyRY_RMF-zgw22eFqmLqVYdS2qL8rJv&export=download',
    'crpKO_irreversible_genes': 'https://drive.google.com/u/0/uc?id=1StH5AYZVHzQOKfP_Kbk6hdJRjBByTkrl&export=download',
    'crpKO_reversible_genes': 'https://drive.google.com/u/0/uc?id=1H7C46n10umCkgiLzcoLFy_6zuXK-LlPF&export=download',
    'crpKO_irrev_results': 'https://drive.google.com/u/0/uc?id=11K6Ok9F3EOn_HVIXG7r3BHrdaj3KjoSX&export=download',
    'attractor_args_d': 'https://drive.google.com/u/0/uc?id=1gN_Sg8x8wYWxMG61QIGh-y6_3NeJKhV-&export=download'
    'gene_status_df': 'https://drive.google.com/u/0/uc?id=15ttPGUhKkNRjvCHKqMZXCYW5ZcwvkgxL&export=download'
    "transcription_logtpm": 'https://drive.google.com/u/0/uc?id=1K77vTyUc4Ie_fR56EKTOjjxlTGZcLgpv&export=download',
    "transcription_metadata": 'https://drive.google.com/u/0/uc?id=1pXv6y6Wh5Q-P9FKj0IeycimRjQJIcMsy&export=download',
    "gsym_thresholds": 'https://drive.google.com/u/0/uc?id=1Brmx1EmdYiQPbdnY-d-YUC_yZVgh5k-a&export=download',
    "gsym_biases": 'https://drive.google.com/u/0/uc?id=1Lixy8qm4jN5N03D7ZMkQeBaDJfiY5dO9&export=download',
    "gsym_zero_biases": 'https://drive.google.com/u/0/uc?id=1Brmx1EmdYiQPbdnY-d-YUC_yZVgh5k-a&export=download'
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
