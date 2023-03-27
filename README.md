# Stream_crack
Program to decrypt stream ciphers that used the same key.

Before run install all requirements
`pip install requirements.txt`


Usage:
$ python main.py DATA_FILE N_SAMPLES MAX_N SPACE_THRES

        DATA_FILE: STR - path to data file
        
        N_SAMPLES: INT - number of cipher texts encoded with the same key
        
        MAX_N: INT - limit of guessing iterations. Recomended: 5000
        
        SPACE_THRES: INT - minimal score to determine if char is a space. Recomended: 8
