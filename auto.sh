handle_interrupt() {
    echo "Interrupted!"
    exit 1
}
trap 'handle_interrupt' INT

echo $(date +%T)
python3 font_file_to_png.py > log1.log
echo $(date +%T)
python3 png_to_edge_detected.py > log2.log
echo $(date +%T)
python3 training.py > log3.log
echo $(date +%T)
echo "COMPLETE"