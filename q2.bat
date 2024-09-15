@echo off

setlocal EnableDelayedExpansion

set strings[0]=q2_capsuleClassic.lay
set strings[1]=q2_contestClassic.lay
set strings[2]=q2_dangerClassic.lay
set strings[3]=q2_mediumClassic.lay
set strings[4]=q2_mediumClassic2.lay
set strings[5]=q2_minimaxClassic.lay
set strings[6]=q2_openClassic.lay
set strings[7]=q2_originalClassic.lay
set strings[8]=q2_smallClassic.lay
set strings[9]=q2_testClassic.lay
set strings[10]=q2_trappedClassic.lay
set strings[11]=q2_trickyClassic.lay

for /L %%i in (0,1,11) do (
    python pacman.py -l layouts/!strings[%%i]! -p Q2_Agent --timeout=30
)