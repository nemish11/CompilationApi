#!/bin/bash
#if g++ /media/nemish/College/ProjectWork/sem-6-project/compilerAPI/compilerAp/compilerApiApp/static/code.cpp -o /media/nemish/College/ProjectWork/sem-6-project/compilerAPI/compilerApi/compilerApiApp/static/abc.out;
#then
#  ./abc.out <input.txt> output.txt
#  exit
#fi

if g++ $1 -o $2;
then
  $3 <$4> $5
  exit
fi
