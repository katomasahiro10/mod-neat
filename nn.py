import random
import math
import networkx as nx
import matplotlib.pyplot as plt

from const import *
from neuron import *

class NeuralNetwork:
    def __init__(self,):
        # initialize neurons
        self.neurons = []
        for n in range(INPUT_NUM):
            self.neurons.append(Neuron(NeuronType.INPUT))
        for n in range(OUTPUT_NUM):
            self.neurons.append(Neuron(NeuronType.OUTPUT))
        for n in range(MODULATION_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.MODULATION))
        for n in range(NORMAL_NUM_LOWER_LIMIT):
            self.neurons.append(Neuron(NeuronType.NORMAL))

        # initialize connections
        self.connections = []
        connection_id = 0
        for n in range(CONNECTION_NUM_LOWER_LIMIT):
            input_id = random.randint(0, len(self.neurons) -1)
            output_id = random.randint(INPUT_NUM, len(self.neurons) -1)
            self.connections.append(Connetion(connection_id, input_id, output_id ))
            connection_id += 1

    @property
    def output_vector(self):
        output_vector = []
        for n in range(INPUT_NUM, INPUT_NUM + OUTPUT_NUM):
            output_vector.append(self.neurons[n].activation)
        return output_vector

    def get_output(self,input_vector):
        if(len(input_vector) != INPUT_NUM):
            raise Exception('ERROR:num of input_vector is invalid')

        # Set input_vector
        for n in range(INPUT_NUM):
            self.neurons[n].activation = input_vector[n]

        for n in range( len(self.neurons)-1, INPUT_NUM-1, -1):
            activated_sum = 0
            modulated_sum = 0
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    activated_sum += self.neurons[self.connections[c].input_id].activation * self.connections[c].weight
                    modulated_sum += self.neurons[self.connections[c].input_id].modulation * self.connections[c].weight

            if(self.neurons[n].neuron_type != NeuronType.MODULATION):
                self.neurons[n].activation = math.tanh(activated_sum + self.neurons[n].bias)
            else:
                self.neurons[n].modulation = math.tanh(activated_sum + self.neurons[n].bias)

            # if Hebbian or ExHebbian, update weight using modulated_sum
        return self.output_vector

    def show_network(self):

        G=nx.MultiDiGraph()

        for n in range(len(self.neurons)):
            if(self.neurons[n].neuron_type == NeuronType.INPUT):
                pos_string= str(n*2)+ ",10!"
                #label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                label_string = str(n)
                G.add_node(n, color='yellow',size=1.5, pos = pos_string,label=label_string, font_size = 8)
            elif(self.neurons[n].neuron_type == NeuronType.OUTPUT):
                pos_string= str((n - INPUT_NUM) *2)+ ",0!"
                label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                G.add_node(n, color='red',size=1.5, pos = pos_string, label=label_string, fot_size = 8)
            elif(self.neurons[n].neuron_type == NeuronType.MODULATION):
                label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                G.add_node(n, color='blue',size=1.5,label=label_string, fot_size = 8, shape='d')
            elif(self.neurons[n].neuron_type == NeuronType.NORMAL):
                label_string = str(n) + "\n" + str( round(self.neurons[n].bias,2))
                G.add_node(n, color='black',size=1.5,label=label_string, fot_size = 8)

        for c in range(len(self.connections)):
            if(self.connections[c].is_valid == True):
                i = self.connections[c].input_id
                o = self.connections[c].output_id
                w = round(self.connections[c].weight,2)
                G.add_edge(i,o,label=w)

        pos = nx.spring_layout(G,k=0.1)
        nx.draw_networkx(G, pos, with_labels=True, alpha=0.5, size=(10,100))
        nx.nx_agraph.view_pygraphviz(G,prog='fdp')
        
class HebbianNetwork(NeuralNetwork):
    def get_output(self,input_vector):
        if(len(input_vector) != INPUT_NUM):
            raise Exception('ERROR:num of input_vector is invalid')

        # Set input_vector
        for n in range(INPUT_NUM):
            self.neurons[n].activation = input_vector[n]

        for n in range( len(self.neurons)-1, INPUT_NUM-1, -1):
            activated_sum = 0
            modulated_sum = 0
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    activated_sum += self.neurons[self.connections[c].input_id].activation * self.connections[c].weight
                    modulated_sum += self.neurons[self.connections[c].input_id].modulation * self.connections[c].weight

            if(self.neurons[n].neuron_type != NeuronType.MODULATION):
                self.neurons[n].activation = math.tanh(activated_sum + self.neurons[n].bias)
            else:
                self.neurons[n].modulation = math.tanh(activated_sum + self.neurons[n].bias)

            # if Hebbian or ExHebbian, update weight using modulated_sum
            for c in range(len(self.connections)):
                if(self.connections[c].is_valid and self.connections[c].output_id == n):
                    if(modulated_sum == 0):
                        self.connections[c].weight += \
                            EPSIRON * self.neurons[n].activation * self.neurons[ self.connections[c].input_id ].activation
                    elif(modulated_sum != 0):
                        self.connections[c].weight += \
                            modulated_sum * (EPSIRON * self.neurons[n].activation * self.neurons[ self.connections[c].input_id ].activation)

        return self.output_vector

class ExHebbianNetwork:
    pass

if __name__ == '__main__':
    n = HebbianNetwork()
    n.show_network()
    n.get_output([1,1])
    n.show_network()
