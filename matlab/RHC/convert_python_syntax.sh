#! /bin/bash
# the only one argument is the number of critical regions
NCR=$1
echo Ncr=$NCR

# generate matrices.py
text_all=
for ((i=1; i<=NCR; i++))
do
	text_all="${text_all}self.B$i = np.array([$(grep -m1 '' results/B$i.txt | sed 's/\r//g')])\n"
	text_all="${text_all}self.C$i=$(grep -m1 '' results/C$i.txt | sed 's/\r//g')\n"
	text_all="${text_all}self.H$i=np.array([$(sed 's/^/[/g' results/H$i.txt | sed 's/$/],/g' | sed 's/\r//g')])\n"
	text_all="${text_all}self.K$i=np.array([$(sed 's/^/[/g' results/K$i.txt | sed 's/$/],/g' | sed 's/\r//g')])\n"
done

echo -e $text_all > matrices.py

# generate crselect.py
text_all=
space4='    '
for ((i=1; i<=NCR; i++))
do
	if ((i==1)); then
		text_all="${text_all}if"
	else
		text_all="${text_all}elif"
	fi	
	text_all="${text_all} np.all(self.H$i.dot(X) <= self.K$i):\n${space4}U0 = self.B$i.dot(X) + self.C$i\n${space4}self.CR = $i\n"
done

text_all="${text_all}else:\n${space4}print('Error: cannot determine critical region!')\n${space4}return None\n"
echo -e "$text_all" > crselect.py