@echo off

setlocal EnableDelayedExpansion

set strings[0]=q1c_bigSearch.lay
set strings[1]=q1c_boxSearch.lay
set strings[2]=q1c_closed.lay
set strings[3]=q1c_greedySearch.lay
set strings[4]=q1c_mediumDottedMaze.lay
set strings[5]=q1c_mediumSearch.lay
set strings[6]=q1c_oddSearch.lay
set strings[7]=q1c_openSearch.lay
set strings[8]=q1c_smallSearch.lay
set strings[9]=q1c_tinySearch.lay
set strings[10]=q1c_trickySearch.lay

for /L %%i in (0,1,10) do (
    python pacman.py -l layouts/!strings[%%i]! -p SearchAgent -a fn=q1c_solver,prob=q1c_problem --timeout=10
)