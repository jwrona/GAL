#author: Jan Wrona
#email: <xwrona00@stud.fit.vutbr.cz>

#global settings
EXEC="./scc_analysis.py"
REPETITIONS=3
MULTIPLICATION=1000

#single settings
SINGLE_ALGORITHMS=("tarjan" "gabow" "tarjan_nx" "kosaraju_nx")
SINGLE_DENSITIES="0.0,0.2,0.5,0.8,1.0"

#multi settings
MULTI_ALGORITHMS="tarjan,gabow,tarjan_nx,kosaraju_nx"
MULTI_DENSITIES=("0.0" "0.2" "0.5" "0.8" "1.0")

################################################################################
if [ ! -d "results" ]
then
    mkdir "results"
fi

#single algorithm measurements
OUT_PATH="results/single"
if [ ! -d "${OUT_PATH}" ]
then
    mkdir "${OUT_PATH}"
fi

for ALG in "${SINGLE_ALGORITHMS[@]}"
do
    #disabled garbage collector
    "${EXEC}" -o="${OUT_PATH}/${ALG}" -r=${REPETITIONS} -m=${MULTIPLICATION} single --algorithm="${ALG}" --densities="${SINGLE_DENSITIES}"

    #enabled garbage collector
    "${EXEC}" -o="${OUT_PATH}/gc_${ALG}" -r=${REPETITIONS} -m=${MULTIPLICATION} -g single --algorithm="${ALG}" --densities="${SINGLE_DENSITIES}"
done

#multiple algorithms measurements
OUT_PATH="results/multi"
if [ ! -d "${OUT_PATH}" ]
then
    mkdir "${OUT_PATH}"
fi

for DENS in "${MULTI_DENSITIES[@]}"
do
    #disabled garbage collector
    "${EXEC}" -o="${OUT_PATH}/${DENS}" -r=${REPETITIONS} -m=${MULTIPLICATION} multi --algorithms="${MULTI_ALGORITHMS}" --density="${DENS}"

    #enabled garbage collector
    "${EXEC}" -o="${OUT_PATH}/gc_${DENS}" -r=${REPETITIONS} -m=${MULTIPLICATION} -g multi --algorithms="${MULTI_ALGORITHMS}" --density="${DENS}"
done
