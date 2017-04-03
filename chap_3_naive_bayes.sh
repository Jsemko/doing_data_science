#!/bin/bash

if [ $# -eq 1 ]
then
  word=$1
else
  echo "Give only one word"
fi

SPAM_DIR="/media/jeremy/San/Data/Doing_Data_Science/enron1"

cd $SPAM_DIR

Nspam=$(ls -l spam/*.txt | wc -l)
Nham=$(ls -l ham/*.txt | wc -l)
Ntot=$Nspam+$Nham

echo $Nspam spam examples
echo $Nham ham examples

Nword_spam=$(grep -il $word spam/*.txt | wc -l)
Nword_ham=$(grep -il $word ham/*.txt | wc -l)

echo $Nword_spam  spam examples containing $word
echo $Nword_ham  ham examples containing $word

Pspam=$(echo "scale=4; $Nspam / ($Ntot)" | bc)
Pham=$(echo "scale=4; 1 - $Pspam" | bc)
echo
echo "estimated P(spam)" = $Pspam
echo "estimated P(ham)" = $Pham

Pword_spam=$(echo "scale=4; $Nword_spam / $Nspam" | bc)
Pword_ham=$(echo "scale=4; $Nword_ham / $Nham" | bc)
echo "estimated P($word|spam)" = $Pword_spam
echo "estimated P($word|ham)" = $Pword_ham

denom=$(echo "scale=4; $Pword_spam*$Pspam + $Pword_ham*$Pham" | bc)

Pspam_word=$(echo "scale=4; ($Pword_spam * $Pspam) / $denom" | bc)
echo
echo "P(spam|$word) = $Pspam_word"

