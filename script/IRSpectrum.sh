#!/bin/bash
# 最初の引数が IBRION=8 で得られた vasprun.xml
# 二番目の引数が LEPSILON = .TRUE. で得られた vasprun.xml
# 

# PHONOPY = 

PHONOPYIR="${HOME}/src/Phonopy-Spectroscopy/Scripts/phonopy-ir"


phonopy --fc $1 --hdf5
phonopy --dim="1 1 1"  --fc-symmetry --mesh="1 1 1" --eigenvectors --readfc --hdf5
phonopy-vasp-born --dim="1 1 1" $2 > BORN
phonopy --dim="1 1 1" --readfc --hdf5 --fc-symmetry --irreps="0 0 0"
$PHONOPYIR --ir_reps --ir_reps_yaml  irreps.yaml --linewidth=8 --data_format csv
mv IR-Spectrum.png IR-Spectrum.cm-1.png
mv IR-Spectrum.dat IR-Spectrum.cm-1.dat
mv IR-Spectrum.csv IR-Spectrum.cm-1.csv
mv IR-PeakTable.csv IR-PeakTable.cm-1.csv
mv IR-PeakTable.dat IR-PeakTable.cm-1.dat
$PHONOPYIR --freq_units meV --ir_reps --ir_reps_yaml irreps.yaml --linewidth=32 --data_format csv
# "--instrument_broadening <broadening>"　を導入するのも手？
mv IR-Spectrum.png IR-Spectrum.meV.png
mv IR-Spectrum.dat IR-Spectrum.meV.dat
mv IR-Spectrum.csv IR-Spectrum.meV.csv
mv IR-PeakTable.dat IR-PeakTable.meV.dat
mv IR-PeakTable.csv IR-PeakTable.meV.csv



#
cat << ! > anime.conf
ANIME_TYPE = v_sim
ANIME = 0. 0. 0
FORCE_CONSTANTS = READ
FREQUENCY_CONVERSION_FACTOR = 64.65417808234001
# meV unit!
!
phonopy anime.conf --hdf5  --readfc
