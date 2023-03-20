BENCHMARKS=(fillseq,readrandom fillseq,readwhilewriting fillrandom,readrandom fillrandom,readwhilewriting \
            fillrandom,readrandom,seekrandom fillseq,readrandom,overwrite \
            fillseq,readrandom,overwrite,readwhilewriting)

for benchmark in ${BENCHMARKS[@]}; do
  ./default_benchmark.sh $benchmark
  ./trg-sample-benchmark.sh $benchmark
done
