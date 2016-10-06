for i in `seq 1 10`; do
    python3 ../src/faces.py training-A.txt facit-A.txt test-B.txt | java FaceTest2 facit-B.txt & python3 ../src/faces.py training-A.txt facit-A.txt test-B.txt | java FaceTest2 facit-B.txt & python3 ../src/faces.py training-A.txt facit-A.txt test-B.txt | java FaceTest2 facit-B.txt & python3 ../src/faces.py training-A.txt facit-A.txt test-B.txt | java FaceTest2 facit-B.txt
    wait
done