#! /bin/bash
# the only one argument is the number of critical regions
NCR=$1
echo Ncr=$NCR
text_all="#ifndef MATRICES_H_\n#define MATRICES_H_\n"
text_all="${text_all}const int H_rownum[32] = {12,13,12,12,12,13,14,13,13,14,13,12,13,13,13,14,15,14,16,14,14,16,14,14,14,15,16,17,17,17,16,19};\n"

for ((i=1; i<=NCR; i++))
do
	text_all="${text_all}const sc_fixed<11,1,SC_RND,SC_SAT> B$i[7]={$(grep -m1 '' results/B$i.txt)};\n"
	text_all="${text_all}const int C$i[7]={$(sed -e "$ ! s/\r/,/g" results/C$i.txt)};\n"
	text_all="${text_all}const sc_fixed<11,1,SC_RND,SC_SAT> H$i[][7]={$(sed -e "$ ! s/\r/,/g" results/H$i.txt)};\n"
	text_all="${text_all}const int K$i[]={$(sed -e "$ ! s/\r/,/g" results/K$i.txt)};\n"
done

text_all="${text_all}\n#endif\n"
echo -e $text_all > matrices.h
