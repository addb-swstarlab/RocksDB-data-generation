BENCHMARK=$1

# generating directory
DIR="results/default"
[ ! -d $DIR ] && mkdir $DIR

rocksdb/db_bench -key_size=32 -value_size=32768 -num=32736 -max_background_compactions=1 -max_background_flushes=1 -write_buffer_size=1048576 -max_write_buffer_number=2 -min_write_buffer_number_to_merge=1 -compaction_pri=0 -compaction_style=0 -level0_file_num_compaction_trigger=4 -level0_slowdown_writes_trigger=20 -level0_stop_writes_trigger=36 -compression_type=snappy -bloom_locality=0 -open_files=-1 -block_size=4096 -cache_index_and_filter_blocks=0 -max_bytes_for_level_base=4194304 -max_bytes_for_level_multiplier=10 -target_file_size_base=1048576 -target_file_size_multiplier=1 -num_levels=7 -memtable_bloom_size_ratio=0 -compression_ratio=0.5 --benchmarks="${BENCHMARK},compact,stats" --statistics > ${DIR}/${BENCHMARK}.txt
