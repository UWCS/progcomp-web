cat /var/log/apache2/error.log | grep "\[wsgi:error]" | grep for | grep -E "\[(CORRECT|PARTIAL)\]" | sed --regexp-extended "s/\[Wed Nov 09 ([0-9:.]+) 2022\] \[wsgi:error] \[pid [0-9]+] \[remote [0-9.:]+\] (\w+) for ([0-9]+) \((.+)\) (\[CORRECT]|\[PARTIAL]) ([0-9]+) .+/\3\t\4\t\6\t\1\t\5\t\2/g"

python3 winner_finder.py 1 example > results/1/example.txt
python3 winner_finder.py 1 normal > results/1/normal.txt
python3 winner_finder.py 1 people > results/1/people.txt
python3 winner_finder.py 1 rounds > results/1/rounds.txt

python3 winner_finder.py 2 big > results/2/big.txt
python3 winner_finder.py 2 example > results/2/example.txt
python3 winner_finder.py 2 example > results/2/normal.txt

python3 winner_finder.py 3 example > results/3/example.txt
python3 winner_finder.py 3 ignoramus > results/3/ignoramus.txt
python3 winner_finder.py 3 merge > results/3/merge.txt
python3 winner_finder.py 3 mixed > results/3/mixed.txt

python3 winner_finder.py 4 accuracy > results/4/accuracy.txt
python3 winner_finder.py 4 big > results/4/big.txt
python3 winner_finder.py 4 collosal > results/4/collosal.txt
python3 winner_finder.py 4 example > results/4/example.txt