# Simple quotes service

How to run:

    git clone https://github.com/everypony/twicher.git
    cd twicher
    mkdir data
    echo "Some quote" >> data/1.txt
    sbt run

Quotes must be plaintext files, named as `\d+\.txt`, e.g. `1.txt`,
`42.txt` and so on.


