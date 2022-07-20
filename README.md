# Nature-Inspired Optimum-Path Forest

*This repository holds all the necessary code to run the very-same experiments described in the paper "Nature-Inspired Optimum-Path Forest".*

---

## References

If you use our work to fulfill any of your needs, please cite us:

```
@article{afonso:2021,
    title = {Nature-Inspired Optimum-Path Forest},
    author = {Afonso, Luis Claudio Sugi and Rodrigues, Douglas and Papa, João Paulo},
    journal = {Evolutionary Intelligence},
    pages = {},
    year = {2021},
    issn = {1864-5917},
    doi = {https://doi.org/10.1007/s12065-021-00664-0},
}
```

---

## Structure

 * `data`: Folder containing the OPF file format datasets;
 * `models`
   * `heuristics.py`: Defines the possible meta-heuristics that can be used;
 * `utils`
   * `datasetinfo.py`: Stores pertinent information from the dataset;
   * `optimizer.py`: Wraps the optimization task into a single method;
   * `outputter.py`: Converts the optimization history into readable output files;
   * `targets.py`: Implements the objective functions to be optimized.

---

## Package Guidelines

### Installation

Install all the pre-needed requirements using:

```Python
pip install -r requirements.txt
```

## Usage

### Prototypes Optimization

```Python
python prototypes.py -h
```

*Note that `-h` invokes the script helper, which assists users in employing the appropriate parameters.*

### Bash Script

Instead of invoking every script to conduct the experiments, it is also possible to use the provided shell scripts, as follows:

```Bash
./pipeline.sh
```

Such a script will conduct every step needed to accomplish the experimentation used throughout this paper. Furthermore, one can change any input argument that is defined in the script.

---

## Support

We know that we do our best, but it is inevitable to acknowledge that we make mistakes. If you ever need to report a bug, report a problem, talk to us, please do so! We will be available at our bests at this repository or d.rodrigues@unesp.br.

---
