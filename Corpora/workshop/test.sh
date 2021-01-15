#!/bin/bash

python3 fitScript.py test.txt > newTest.txt
diff test.txt newTest.txt
