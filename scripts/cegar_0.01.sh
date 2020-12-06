mkdir results_cegar
mkdir results_cegar/cegar_0.01

(time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_10/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_10.txt
(time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_100/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_100.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_150/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_150.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_20/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_20.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_200/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_200.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_30/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_30.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_40/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_40.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_5/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_5.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_50/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_50.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_60/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_60.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_70/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_70.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_80/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_80.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_3_90/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_3_90.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_10/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_10.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_100/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_100.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_150/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_150.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_20/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_20.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_200/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_200.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_30/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_30.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_40/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_40.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_5/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_5.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_50/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_50.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_60/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_60.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_70/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_70.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_80/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_80.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_4_90/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_4_90.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_10/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_10.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_100/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_100.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_150/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_150.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_20/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_20.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_200/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_200.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_30/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_30.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_40/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_40.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_5/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_5.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_50/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_50.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_60/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_60.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_70/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_70.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_80/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_80.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_5_90/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_5_90.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_10/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_10.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_100/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_100.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_150/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_150.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_20/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_20.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_200/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_200.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_30/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_30.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_40/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_40.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_5/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_5.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_50/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_50.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_60/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_60.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_70/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_70.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_80/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_80.txt
# (time python -u source/run_eran.py --spec benchmark/cegar/nnet/mnist_relu_6_90/spec.json --algorithm deepcegar --eps 0.01 --dataset mnist_fc) &> results_cegar/cegar_0.01/log_mnist_relu_6_90.txt
