@echo off

setlocal EnableDelayedExpansion

set strings[0]=q1a_bigMaze.lay
set strings[1]=q1a_bigMaze2.lay
set strings[2]=q1a_contoursMaze.lay
set strings[3]=q1a_mediumMaze.lay
set strings[4]=q1a_mediumMaze2.lay
set strings[5]=q1a_openMaze.lay
set strings[6]=q1a_smallMaze.lay
set strings[7]=q1a_testMaze.lay
set strings[8]=q1a_tinyMaze.lay
set strings[9]=q1a_trickyMaze.lay

for /L %%i in (0,1,9) do (
    python pacman.py -l layouts/!strings[%%i]! -p SearchAgent -a fn=q1a_solver,prob=q1a_problem --timeout=1
)
