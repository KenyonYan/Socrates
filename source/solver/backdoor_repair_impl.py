import autograd.numpy as np
import cvxpy as cp
import multiprocessing
import ast
import os
import time
import random
import math

import gurobipy as gp
from gurobipy import GRB

from scipy.optimize import minimize
from scipy.optimize import Bounds
from autograd import grad
from assertion.lib_functions import di
from utils import *
from poly_utils import *
from solver.refinement_impl import Poly

import matplotlib.pyplot as plt


class BackDoorRepairImpl():
    def __solve_backdoor_repair(self, model, spec, display):
        target = spec['target']
        rate = spec['rate']

        total_imgs = spec['total_imgs']
        num_repair = spec['num_repair']
        dataset = spec['dataset']

        known_stamp = spec['known_stamp']

        y0s = np.array(ast.literal_eval(read(spec['pathY'])))
        valid_x0s = self.__get_valid_x0s(model, total_imgs, y0s, spec['pathX'], target)

        if len(valid_x0s) == 0:
            print('No data to analyze target = {}'.format(target))
            return None, None

        print('Number of valid_x0s = {} for target = {}'.format(len(valid_x0s), target))

        print('Lower bound = {} and Upper bound = {}'.format(model.lower[0], model.upper[0]))

        if known_stamp:
            position = spec['stamp_pos']
            size = spec['stamp_size']

            print('\nPredefine stamp position = {} with target = {}'.format(position, target))

            backdoor_indexes = self.__get_backdoor_indexes(size, position, dataset)
            print('\nStamp indexes = {}'.format(backdoor_indexes))

            if dataset == 'mnist':
                trigger = np.zeros(1 * 28 * 28)
                mask = np.zeros(1 * 28 * 28)
            elif dataset == 'cifar':
                trigger = np.zeros(3 * 32 * 32)
                mask = np.zeros(3 * 32 * 32)

            trigger[backdoor_indexes] = 1.0
            mask[backdoor_indexes] = 1.0
        else:
            print('\nGenerate reversed trigger with target = {}'.format(target))
            stamp = self.__attack(model, valid_x0s, target, dataset)

            if dataset == 'mnist':
                trigger = stamp[:(1 * 28 * 28)]
                mask = stamp[(1 * 28 * 28):]
            elif dataset == 'cifar':
                trigger = stamp[:(3 * 32 * 32)]
                mask = stamp[(3 * 32 * 32):]

            print('trigger = {}'.format(trigger))
            print('mask = {}'.format(mask))
            print('sum mask = {}\n'.format(np.sum(mask)))

        valid_x0s_with_bd, successful_atk_cnt = self.__get_x0s_with_bd(model, valid_x0s, trigger, mask, target)

        print('len(valid_x0s) =', len(valid_x0s))
        print('len(valid_x0s_with_bd) =', len(valid_x0s_with_bd))
        print('successful_atk_cnt =', successful_atk_cnt)

        if successful_atk_cnt / len(valid_x0s) < rate:
            print('\nrate = {}'.format(successful_atk_cnt / len(valid_x0s)))
            print('The stamp does not satisfy the success rate = {} with target = {}'.format(rate, target))
        else:
            print('The stamp satisfies the success rate = {} with target = {}'.format(rate, target))
            res = self.__clean_backdoor(model, valid_x0s, valid_x0s_with_bd, trigger, mask, target, num_repair)

            if res is not None:
                opt, repair_layer, repair_neuron = res

                print(repair_layer)
                print(repair_neuron)

                print('old weights = {}'.format(model.layers[repair_layer].weights[:,repair_neuron]))
                print('old bias = {}'.format(model.layers[repair_layer].bias[0,repair_neuron]))

                new_model = model.copy()
                num_weis = len(model.layers[repair_layer].weights[:,repair_neuron])
                print('num_weis = {}'.format(num_weis))
                self.__get_new_weights_and_bias(new_model, opt, repair_layer, repair_neuron, num_weis)

                print('new weights = {}'.format(new_model.layers[repair_layer].weights[:,repair_neuron]))
                print('new bias = {}'.format(new_model.layers[repair_layer].bias[0,repair_neuron]))

                new_valid_x0s = self.__get_valid_x0s(new_model, total_imgs, y0s, spec['pathX'], target)
                new_valid_x0s_with_bd, new_successful_atk_cnt = self.__get_x0s_with_bd(new_model, new_valid_x0s, trigger, mask, target)

                print('len(new_valid_x0s) =', len(new_valid_x0s))
                print('len(new_valid_x0s_with_bd) =', len(new_valid_x0s_with_bd))
                print('new_successful_atk_cnt =', new_successful_atk_cnt)

        return None, None


    def __get_backdoor_indexes(self, size, position, dataset):
        if position < 0:
            return None

        if dataset == 'mnist':
            num_chans, num_rows, num_cols = 1, 28, 28
        elif dataset == 'cifar':
            num_chans, num_rows, num_cols = 3, 32, 32

        row_idx = int(position / num_cols)
        col_idx = position - row_idx * num_cols

        if row_idx + size > num_rows or col_idx + size > num_cols:
            return None

        indexes = []

        for i in range(num_chans):
            tmp = position + i * num_rows * num_cols
            for j in range(size):
                for k in range(size):
                    indexes.append(tmp + k)
                tmp += num_cols

        return indexes


    def __get_new_weights_and_bias(self, new_model, opt, repair_layer, repair_neuron, num_weis):
        opt.write('model.sol')

        for idx in range(num_weis):
            var = opt.getVarByName('w' + str(idx))
            new_model.layers[repair_layer].weights[idx,repair_neuron] = var.x

        var = opt.getVarByName('b')
        new_model.layers[repair_layer].bias[0,repair_neuron] = var.x


    def __clean_backdoor(self, model, valid_x0s, valid_x0s_with_bd, trigger, mask, target, num_repair):
        print('\nBegin cleansing')
        # assert self.__validate(model, valid_x0s_with_bd, trigger, mask, target, 1.0)

#####################################################################################################################################
        number_of_layers = len(model.layers)

        ie_ave_matrix = []

        for do_layer in range(number_of_layers - 1): # not consider the last layer

            if model.layers[do_layer].is_linear_layer():
                number_of_neurons = model.layers[do_layer].get_number_neurons()

                for do_neuron in range(number_of_neurons):
                    ie, min_val, max_val = self.get_ie_do_h_dy(model, valid_x0s_with_bd, trigger, mask, target, do_layer, do_neuron)
                    mie = np.mean(np.array(ie))

                    if mie > 0.0:
                        new_entry = []
                        new_entry.append(mie)
                        new_entry.append(do_layer)
                        new_entry.append(do_neuron)
                        
                        ie_ave_matrix.append(new_entry)

        print(ie_ave_matrix)
        ie_ave_matrix.sort(reverse=True)
        print()
        print(ie_ave_matrix)

        repair_layers, repair_neurons = [], []
        for i in range (0, num_repair):
            repair_layers.append(int(ie_ave_matrix[i][1]))
            repair_neurons.append(int(ie_ave_matrix[i][2]))
        
        print('\nRepair layers: {}'.format(repair_layers))
        print('Repair neurons: {}'.format(repair_neurons))

        min_weight, max_weight, min_bias, max_bias = self.__collect_min_max_value(model)

        print('\nmin_weight = {}, max_weight = {}'.format(min_weight, max_weight))
        print('min_bias = {}, max_bias = {}\n'.format(min_bias, max_bias))

        for repair_layer, repair_neuron in list(zip(repair_layers, repair_neurons)):
            self.__write_problem(model, valid_x0s, valid_x0s_with_bd, trigger, mask, target, repair_layer, repair_neuron,
                min_weight, max_weight, min_bias, max_bias)

            filename = 'prob.lp'
            opt = gp.read(filename)
            opt.setParam(GRB.Param.DualReductions, 0)

            opt.optimize()
            # os.remove(filename)

            if opt.status == GRB.INFEASIBLE:
                print('Infeasible')
                # os.remove(filename)
            elif opt.status == GRB.OPTIMAL:
                print('Optimal')
                # os.remove(filename)
                return opt, repair_layer, repair_neuron

        return None


    def __collect_min_max_value(self, model):
        max_weight, max_bias, coef = 0.0, 0.0, 1.0

        for layer in model.layers:
            if layer.is_linear_layer():
                max_weight = max(max_weight, np.max(np.abs(layer.weights)))
                max_bias = max(max_bias, np.max(np.abs(layer.bias)))

        return -coef * max_weight, coef * max_weight, -coef * max_bias, coef * max_bias


    def __write_bounds(self, prob, lw_coll, up_coll, min_weight, max_weight, min_bias, max_bias, num_weis):
        for idx in range(num_weis):
            prob.write('  {} <= w{} <= {}\n'.format(min_weight, idx, max_weight))
        prob.write('  {} <= b <= {}\n'.format(min_bias, max_bias))

        for cnt_imgs in range(len(lw_coll)):
            lw_list = lw_coll[cnt_imgs]
            up_list = up_coll[cnt_imgs]

            for var_idx in range(len(lw_list)):
                lw, up = lw_list[var_idx], up_list[var_idx]
                if lw == up:
                    prob.write('  x{}_{} = {}\n'.format(var_idx, cnt_imgs, lw))
                else:
                    prob.write('  {} <= x{}_{} <= {}\n'.format(lw, var_idx, cnt_imgs, up))

        prob.flush()


    def __write_binary(self, prob, bins_coll):
        prob.write(' ')
        for cnt_imgs in range(len(bins_coll)):
            for idx in range(bins_coll[cnt_imgs]):
                prob.write(' a{}_{}'.format(idx, cnt_imgs))


    def __write_problem(self, model, valid_x0s, valid_x0s_with_bd, trigger, mask, target,
            repair_layer, repair_neuron, min_weight, max_weight, min_bias, max_bias):
        filename = 'prob.lp'
        prob = open(filename, 'w')

        prob.write('Minimize\n')
        prob.write('  0\n')

        lw_coll, up_coll, bins_coll = [], [], []

        prob.write('Subject To\n')

        cnt_imgs, has_bins = 0, False

        # original input
        for x_0, output_x0 in valid_x0s:
            input_repair = model.apply_to(x_0, repair_layer).reshape(-1)
            y0 = np.argmax(output_x0)

            lw_list, up_list, num_bins = self.__write_constr(prob, model, input_repair, repair_layer, repair_neuron,
                min_weight, max_weight, min_bias, max_bias, cnt_imgs, y0)

            if num_bins > 0: has_bins = True
            
            lw_coll.append(lw_list)
            up_coll.append(up_list)
            bins_coll.append(num_bins)
            
            cnt_imgs += 1

        # input with backdoor
        for x_0, x_bd, output_x0, output_x_bd in valid_x0s_with_bd:
            input_repair = model.apply_to(x_bd, repair_layer).reshape(-1)
            y0 = np.argmax(output_x0)

            lw_list, up_list, num_bins = self.__write_constr(prob, model, input_repair, repair_layer, repair_neuron,
                min_weight, max_weight, min_bias, max_bias, cnt_imgs, y0)

            if num_bins > 0: has_bins = True
            
            lw_coll.append(lw_list)
            up_coll.append(up_list)
            bins_coll.append(num_bins)
            
            cnt_imgs += 1

        prob.write('Bounds\n')
        self.__write_bounds(prob, lw_coll, up_coll, min_weight, max_weight, min_bias, max_bias, len(input_repair))

        if has_bins:
            prob.write('Binary\n')
            self.__write_binary(prob, bins_coll)

        prob.write('\nEnd\n')

        prob.flush()
        prob.close()


    def __write_constr(self, prob, model, input_repair, repair_layer, repair_neuron,
            min_weight, max_weight, min_bias, max_bias, cnt_imgs, y0):
        lw_list, up_list = [], []
        lw_input, up_input = [], []
        num_bins = 0

        for input_val in input_repair:
            lw_input.append(input_val)
            up_input.append(input_val)

        lw_list.append(lw_input)
        up_list.append(up_input)

        curr_var_idx = len(input_repair)
        prev_var_idx = 0

        for layer_idx in range(repair_layer, len(model.layers)):
            layer = model.layers[layer_idx]
            lw_layer, up_layer = [], []

            # fully connected layer
            if layer.is_linear_layer():
                weights = layer.weights.transpose(1, 0) # shape: num_neuron X input
                bias = layer.bias.transpose(1, 0).reshape(-1) # shape: num_neuron

                # repair layer
                if layer_idx == repair_layer:
                    for neuron_idx in range(len(bias)):
                        # repair neuron
                        if neuron_idx == repair_neuron:
                            # compute bounds
                            lw, up = 0.0, 0.0

                            for input_val in input_repair:
                                if input_val > 0:
                                    lw += min_weight * input_val
                                    up += max_weight * input_val
                                elif input_val < 0:
                                    lw += max_weight * input_val
                                    up += min_weight * input_val

                            lw, up = lw + min_bias, up + max_bias
                            assert lw <= up

                            lw_layer.append(lw)
                            up_layer.append(up)

                            # write constraints
                            prob.write('  x{}_{}'.format(curr_var_idx + neuron_idx, cnt_imgs))
                            # input vals are coefs, weights and bias are variables
                            coefs = -input_repair
                            for coef_idx in range(len(coefs)):
                                coef = coefs[coef_idx]
                                if coef > 0.0:
                                    prob.write(' + {} w{}'.format(coef, coef_idx))
                                elif coef < 0.0:
                                    prob.write(' - {} w{}'.format(abs(coef), coef_idx))
                            prob.write(' - b = 0.0\n')
                        # other neurons
                        else:
                            # concrete values for other neurons
                            val = (np.sum(weights[neuron_idx] * input_repair) + bias[neuron_idx])

                            lw_layer.append(val)
                            up_layer.append(val)
                # other linear layers
                else:
                    lw_prev, up_prev = lw_list[-1], up_list[-1]

                    for neuron_idx in range(len(bias)):
                        # compute bounds
                        lw, up = 0.0, 0.0

                        for weight_idx in range(len(weights[neuron_idx])):
                            weight_val = weights[neuron_idx][weight_idx]
                            if weight_val > 0:
                                lw += weight_val * lw_prev[weight_idx]
                                up += weight_val * up_prev[weight_idx]
                            elif weight_val < 0:
                                lw += weight_val * up_prev[weight_idx]
                                up += weight_val * lw_prev[weight_idx]

                        lw, up = lw + bias[neuron_idx], up + bias[neuron_idx]
                        assert lw <= up

                        lw_layer.append(lw)
                        up_layer.append(up)

                        # write constraints
                        prob.write('  x{}_{}'.format(curr_var_idx + neuron_idx, cnt_imgs))
                        coefs = -weights[neuron_idx]
                        for coef_idx in range(len(coefs)):
                            coef = coefs[coef_idx]
                            if coef > 0.0:
                                prob.write(' + {} x{}_{}'.format(coef, prev_var_idx + coef_idx, cnt_imgs))
                            elif coef < 0.0:
                                prob.write(' - {} x{}_{}'.format(abs(coef), prev_var_idx + coef_idx, cnt_imgs))
                        prob.write(' = {}\n'.format(bias[neuron_idx]))
            # ReLU
            else:
                lw_prev, up_prev = lw_list[-1], up_list[-1]

                for neuron_idx in range(len(lw_prev)):
                    # compute bounds
                    lw, up = lw_prev[neuron_idx], up_prev[neuron_idx]
                    assert lw <= up

                    lw_layer.append(max(lw, 0.0))
                    up_layer.append(max(up, 0.0))

                    # write constraints
                    if lw < 0.0 and up > 0.0:
                        cvar_idx = curr_var_idx + neuron_idx
                        pvar_idx = prev_var_idx + neuron_idx

                        prob.write('  x{}_{} - x{}_{} + {} a{}_{} <= {}\n'.format(cvar_idx, cnt_imgs, pvar_idx, cnt_imgs, -lw, num_bins, cnt_imgs, -lw))
                        prob.write('  x{}_{} - x{}_{} >= 0.0\n'.format(cvar_idx, cnt_imgs, pvar_idx, cnt_imgs))
                        prob.write('  x{}_{} - {} a{}_{} <= 0.0\n'.format(cvar_idx, cnt_imgs, up, num_bins, cnt_imgs))
                        prob.write('  x{}_{} >= 0.0\n'.format(cvar_idx, cnt_imgs))
                        num_bins += 1
                    elif lw >= 0.0:
                        prob.write('  x{}_{} - x{}_{} = 0.0\n'.format(curr_var_idx + neuron_idx, cnt_imgs, prev_var_idx + neuron_idx, cnt_imgs))

            lw_list.append(lw_layer)
            up_list.append(up_layer)

            prev_var_idx = curr_var_idx
            curr_var_idx += len(lw_layer)

        # output constraints
        for output_idx in range(len(lw_list[-1])):
            if output_idx != y0:
                # use 0.001 to guarantee the output condition
                prob.write('  x{}_{} - x{}_{} > 0.001\n'.format(prev_var_idx + y0, cnt_imgs, prev_var_idx + output_idx, cnt_imgs))

        flat_lw_list = [item for sublist in lw_list for item in sublist]
        flat_up_list = [item for sublist in up_list for item in sublist]

        prob.flush()

        return flat_lw_list, flat_up_list, num_bins


    def get_ie_do_h_dy(self, model, valid_x0s_with_bd, trigger, mask, target, do_layer, do_neuron):
        # get value range of given hidden neuron

        hidden_max, hidden_min = None, None

        for x0, x_bd, output_x0, output_x_bd in valid_x0s_with_bd:
            _, hidden = model.apply_get_h(x_bd, do_layer, do_neuron)

            if hidden_max is None:
                hidden_max = hidden
                hidden_min = hidden
            else:
                if hidden > hidden_max:
                    hidden_max = hidden
                if hidden < hidden_min:
                    hidden_min = hidden

        # now we have hidden_min and hidden_max

        # compute interventional expectation for each step
        ie, num_step = [], 16
        if hidden_max == hidden_min:
            ie = [hidden_min] * num_step
        else:
            for h_val in np.linspace(hidden_min, hidden_max, num_step):
                dy = self.get_dy_do_h(model, valid_x0s_with_bd, trigger, mask, target, do_layer, do_neuron, h_val)
                ie.append(dy)

        return ie, hidden_min, hidden_max

    #
    # get expected value of y with hidden neuron intervention
    #
    def get_dy_do_h(self, model, valid_x0s_with_bd, trigger, mask, target, do_layer, do_neuron, do_value):
        dy_sum = 0.0

        for x0, x_bd, output_x0, output_x_bd in valid_x0s_with_bd:
            output_do = model.apply_intervention(x_bd, do_layer, do_neuron, do_value).reshape(-1)

            dy = abs(output_x_bd[target] - output_do[target])
            dy_sum = dy_sum + dy

        avg = dy_sum / len(valid_x0s_with_bd)

        return avg
#####################################################################################################################################


    def __get_valid_x0s(self, model, total_imgs, y0s, path, target):
        valid_x0s = []

        for i in range(total_imgs):
            pathX = path + 'data' + str(i) + '.txt'
            x0 = np.array(ast.literal_eval(read(pathX)))

            output_x0 = model.apply(x0).reshape(-1)
            y0 = np.argmax(output_x0)

            if i < 10:
                print('\n==============\n')
                print('Data {}\n'.format(i))
                print('x0 = {}'.format(x0))
                print('output_x0 = {}'.format(output_x0))
                print('y0 = {}'.format(y0))
                print('y0s[i] = {}\n'.format(y0s[i]))

            if y0 == y0s[i] and y0 != target:
                valid_x0s.append((x0, output_x0))

        return valid_x0s


    def __get_x0s_with_bd(self, model, valid_x0s, trigger, mask, target):
        valid_x0s_with_bd = []
        successful_atk_cnt = 0

        for i in range(len(valid_x0s)):
            x0, output_x0 = valid_x0s[i]

            x_bd = (1 - mask) * x0 + mask * trigger

            output_x_bd = model.apply(x_bd).reshape(-1)
            target_x_bd = np.argmax(output_x_bd)

            if target_x_bd == target: successful_atk_cnt += 1
            valid_x0s_with_bd.append((x0, x_bd, output_x0, output_x_bd))

        return valid_x0s_with_bd, successful_atk_cnt


    # def __validate(self, model, valid_x0s_with_bd, trigger, mask, target, rate):
    #     cnt = 0

    #     for x0, x_bd, output_x0, output_x_bd in valid_x0s_with_bd:
    #         xi = (1 - mask) * x0 + mask * trigger
    #         output = model.apply(xi).reshape(-1)

    #         assert np.all(xi == x_bd)
    #         assert np.all(output == output_x_bd)

    #         if np.argmax(output) == target: # attack successfully
    #             cnt += 1

    #     return (cnt / len(valid_x0s_with_bd)) >= rate


    def __attack(self, model, valid_x0s, target, dataset):
        def obj_func(x, model, valid_x0s, target, length, half_len):
            res, lam = 0.0, 1.0

            for x0, output_x0 in valid_x0s:
                trigger = x[:half_len] # trigger
                mask = x[half_len:] # mask
                
                xi = (1 - mask) * x0 + mask * trigger

                output = model.apply(xi).reshape(-1)
                target_score = output[target]

                output_no_target = output - np.eye(len(output))[target] * 1e9
                max_score = np.max(output_no_target)

                if target_score > max_score:
                    res += 0
                else:
                    res += max_score - target_score + 1e-9

            res += lam * np.sum(mask)

            return res

        if dataset == 'mnist':
            length = 2 * 28 * 28
        elif dataset == 'cifar':
            length = 6 * 32 * 32
        
        half_len = length // 2

        lw = np.zeros(length) # mask and trigger
        up = np.full(length, 1.0) # mask and trigger

        lw[:half_len] = model.lower # lower for trigger
        up[:half_len] = model.upper # upper for trigger

        x = np.zeros(length)

        args = (model, valid_x0s, target, length, half_len)
        jac = grad(obj_func)
        bounds = Bounds(lw, up)

        res = minimize(obj_func, x, args=args, jac=jac, bounds=bounds)
        # print('res.fun = {}'.format(res.fun))

        return res.x


    def __run(self, model, idx, lst_poly):
        if idx == len(model.layers):
            return None
        else:
            poly_next = model.forward(lst_poly[idx], idx, lst_poly)
            lst_poly.append(poly_next)
            return self.__run(model, idx + 1, lst_poly)


    def solve(self, model, assertion, display=None):
        return self.__solve_backdoor_repair(model, assertion, display)
