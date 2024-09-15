@echo off

setlocal EnableDelayedExpansion

set strings[0]=q1b_bigCorners.lay
set strings[1]=q1b_mediumCorners2.lay
set strings[2]=q1b_tinyCorners.lay
set strings[3]=q1b_bigCorners2.lay
set strings[4]=q1b_openCorners.lay
set strings[5]=q1b_tinyCorners2.lay
set strings[6]=q1b_closed.lay
set strings[7]=q1b_openCorners2.lay
set strings[8]=q1b_trickyCorners.lay
set strings[9]=q1b_mediumCorners.lay
set strings[10]=q1b_smallCorners.lay

for /L %%i in (0,1,10) do (
    python pacman.py -l layouts/!strings[%%i]! -p SearchAgent -a fn=q1b_solver,prob=q1b_problem --timeout=5
)
