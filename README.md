This repository supports a research project on negation scope resolution using cross-lingual transfer learning. Negation is a complex, universal linguistic phenomenon that presents significant challenges for both cognitive and computational processing. Accurate handling of negation is critical for applications such as biomedical text mining, sentiment analysis, and machine translation. While most prior work has focused on English, this project explores cross-lingual negation scope resolution in English, French, Spanish, and Russian. The Russian test set was annotated specifically for the project using the Prodigy tool and is publicly available here: 🔗 [SherlockBox-RuNeg](https://zenodo.org/records/4537834)

The work investigates both zero-shot and low-resource fine-tuning scenarios leveraging multilingual BERT (mBERT) and XLM-RoBERTa. Results show strong performance, with zero-shot F1-scores as high as 86.86% (Spanish to Russian) and 84.73% (English to French). In addition to practical experiments, this work offers a detailed analysis of model outputs in the context of negation typology and lexical capacity.

## Publications

1. **Cross-lingual transfer-learning approach to negation scope resolution**  
   Presented at SwissText 2020  
   📄 [Read the paper (CEUR-WS)](https://ceur-ws.org/Vol-2624/paper13.pdf)

2. **Negation typology and general representation models for cross-lingual zero-shot negation scope resolution in Russian, French, and Spanish**  
   Published in the NAACL 2021 Student Research Workshop  
   📄 [Read the paper (ACL Anthology)](https://aclanthology.org/2021.naacl-srw.3/)


---

## negex_scripts

The original **NegEx** algorithm was created by Chapman et al. (2001) and adapted for Python by Peter Khang. This is a rule-based algorithm that is used as a baseline. My NegEx adaptation works with `.json` files and does not consider potential cues. It assigns numeric scope labels to all tokens in a sentence and calculates the F1-score for scope tokens.

- `wrapper.py`  
- `negex_baseline.py`  
- `extract_french_cues4negex.py`:  
  Performs cue manipulations described in Section 7.1 and writes a new list of triggers for NegEx.

---

## server-scripts

Fine-tuning and testing transformer models was performed on an institutional server as well as on  
[Google Drive](https://drive.google.com/drive/folders/1md-_WBrg9x2Kp4g6jNExLJrEt5HBGL23?usp=sharing). The original **NegBERT** architecture was created by Khandelwal and Sawant (2020). 

- `NegBERT_reduced.ipynb`:  
  A shortened and consolidated version of the original NegBERT script for my use.

- `train_json_scope.ipynb`:  
  Includes part of the NegBERT architecture for training a scope model.  
  Differences from the original: works with mBERT, accepts intermediary representations in JSON,  
  shuffles input, and saves a trained model.

- `test_json_scope.ipynb`:  
  Includes part of the NegBERT architecture for testing a scope model.  
  Differences from the original: works with mBERT, accepts intermediary JSON input,  
  loads a saved model, and writes output to a TXT file.

---

## scripts

Language-based preprocessing and analysis scripts. For example:

- `count_lexical_overlap.py`:  
  Calculates Jaccard Index (Section 8.5). Provides vocabulary size and lexical overlap (Table 7).  
  Prints a sample of mBERT’s vocabulary (Fig. 13).

- `analyze_french_scope_stoppers.py`:  
  Extracts information for Table 8. Counts number of types and tokens in gold and mBERT annotation.

- `analyze_spanish_scope_stoppers.py`:  
  Extracts info for Table 9. Assigns POS to Spanish scope stoppers and counts types/tokens in gold and mBERT annotation.

- `count_sins.py`:  
  Extracts info about Spanish cues and their scopes (Tables 10 and 12).

- `syntax_parser.py`:  
  Parses English and French sentences and generates visualizations of constituency trees.  
  Requires installation of the `benepar` package.

- `extract_spanishSFU2MultiBERT.py`:  
  Parses Spanish SFU corpus. Extracts sentences with only one negation event (OneScopeSP).  
  Transforms data into vectors of tokens, cue labels, and scope labels. Splits data into `sp100` and `spXX`.

- `preprocess_eng_corpora.ipynb`:  
  A modified version of NegBERT’s Data class to convert the English corpora (Sherlock, SFU, and Bioscope)  
  into three vectors per sentence: tokens, cue labels, scope labels. Outputs intermediary representations to JSON files.

- `extract_data_sherlock.py`:  
  Uses a function from NegBERT to convert each sentence into 3 vectors and saves them to a JSON file.  
  Calculates cue distribution for Fig. 8 and writes it to a TXT file.

- `extract_OneScopeFR_from_CAS.py`:  
  Extracts French sentences with only one negation (OneScopeFR) from CAS.

- `extract_and_split_french.py`:  
  Converts French data into token, cue, and scope vectors. Randomly splits data into `fr100` and `frXX`.


## prodigy+prep

Scripts for annotating Russian data using Prodigy.


## Citation

If you use this repository or its methods, please cite the following works:

```bibtex
@inproceedings{Shaitarova2020,
  title={Cross-Lingual Transfer-Learning Approach to Negation Scope Resolution},
  author={Shaitarova, Anastassia and Furrer, Lenz and Rinaldi, Fabio},
  booktitle={CEUR Workshop Proceedings},
  year={2020},
  publisher={CEUR-WS},
  address={Zurich},
  url={https://doi.org/10.5167/uzh-197355}
}

@inproceedings{Shaitarova2021,
  title={Negation Typology and General Representation Models for Cross-Lingual Zero-Shot Negation Scope Resolution in Russian, French, and Spanish},
  author={Shaitarova, Anastassia and Rinaldi, Fabio},
  booktitle={Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Student Research Workshop},
  pages={15--23},
  year={2021},
  organization={Association for Computational Linguistics},
  address={Online},
  url={https://www.aclweb.org/anthology/2021.naacl-srw.3}
}

