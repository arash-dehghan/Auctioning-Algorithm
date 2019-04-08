import random
from random import shuffle


"""
The following is code impliments both the naive and sophisticated auctioning algorithm which is based on the MIT paper "Auction Algorithms" also included. The goal of this algorithm is to take a game theory approach (Thinking of something similar to the matching problem), attempting to find the optimal payoff matching for the agents, considering their values of objects, and the costs of the objects the agents are bidding on.
"""
random.seed(918)

def create_matrices(number_of_agents):
    """
    Create matrices of agents and their values for varying objects
    """
    matrix = []
    agent = 0
    while agent != number_of_agents:
        temp_matrix = []
        for prices in range(0,number_of_agents):
            temp_matrix.append(round(random.uniform(1, 15),0))
        matrix.append(temp_matrix)
        agent += 1
    prices_list = []
    for prices in range(0,number_of_agents):
        prices_list.append(round(random.uniform(1, 10),0))
    return matrix, prices_list

def assign_values(number_of_agents):
    """
    Assign the values to each of the agents
    """
    temp_list = []
    agents = []
    for i in range(0,number_of_agents):
        temp_list.append(i)
    shuffle(temp_list)
    for p in range(0,number_of_agents):
        agents.append([temp_list[p],0])
    return agents

def get_best_option(agent_number,matrix,costs):
    """
    Find the best option for the given agent
    """
    diff_list = []
    for i in range(0,len(costs)):
        diff_list.append(matrix[agent_number][i] - costs[i])
    highest_val = max(diff_list)
    ind_highest_val = diff_list.index(highest_val)
    diff_list[ind_highest_val] = -1000000000
    second_highest_val = max(diff_list)
    ind_second_highest_val = diff_list.index(max(diff_list))
    return highest_val,ind_highest_val,second_highest_val,ind_second_highest_val

def find_index_of_val(mylist,value):
    """
    Find index of given value in list
    """
    l = [i[0] for i in mylist]
    return l.index(value)

def check_happiness(agent_matrix,payoff,cost):
    """
    Check if agents are happy with their current situation
    """
    for i in range(0,len(agent_matrix)):
        if agent_matrix[i][1] == 0:
            high,ind_high,sec_high,sec_ind_high = get_best_option(i,payoff_matrix,cost_list)
            if ind_high == agent_matrix[i][0]:
                agent_matrix[i][1] = 1

def naive_auction(agents,payoff_matrix,cost_list):
    """
    Running the naive version of the auction algorithm where we do not force agents to increase bids by epsilon each time they bid
    """
    while sum(n for _, n in agents) != len(agents):
        for i in range(0,len(agents)):
            check_happiness(agents,payoff_matrix,cost_list)
            if agents[i][1] == 0:
                high,ind_high,sec_high,sec_ind_high = get_best_option(i,payoff_matrix,cost_list)
                switch_index = find_index_of_val(agents,int(ind_high))
                agents[switch_index][1] = 0
                agents[i][1] = 1
                agents[switch_index][0] = agents[i][0]
                agents[i][0] = ind_high
                cost_list[ind_high] = cost_list[ind_high] + abs(((payoff_matrix[i][ind_high] - cost_list[ind_high]) - (payoff_matrix[i][sec_ind_high] - cost_list[sec_ind_high])))
    for agent in range(0,len(cost_list)):
        print("Agent {} will pay ${} for object {}. Their original value of this object was ${}".format(agent,cost_list[agents[agent][0]], agents[agent][0], payoff_matrix[agent][agents[agent][0]]))

def sophisticated_auction(epsilon, agents,payoff_matrix, cost_list):
    """
    Running the sophisticated version of the auction algorithm where we force agents to increase bids by epsilon each time they bid
    """
    while sum(n for _, n in agents) != len(agents):
        for i in range(0,len(agents)):
            check_happiness(agents,payoff_matrix,cost_list)
            if agents[i][1] == 0:
                high,ind_high,sec_high,sec_ind_high = get_best_option(i,payoff_matrix,cost_list)
                switch_index = find_index_of_val(agents,int(ind_high))
                agents[switch_index][1] = 0
                agents[i][1] = 1
                agents[switch_index][0] = agents[i][0]
                agents[i][0] = ind_high
                cost_list[ind_high] = cost_list[ind_high] + abs(((payoff_matrix[i][ind_high] - cost_list[ind_high]) - (payoff_matrix[i][sec_ind_high] - cost_list[sec_ind_high]))) + epsilon
    for agent in range(0,len(cost_list)):
        print("Agent {} will pay ${} for object {}. Their original value of this object was ${}".format(agent,round(cost_list[agents[agent][0]],2), agents[agent][0], payoff_matrix[agent][agents[agent][0]]))

N = 10
epsilon = 0.01
agents = assign_values(N)
payoff_matrix, cost_list = create_matrices(N)

# agents = [[0,0],[2,0],[1,0]]
# payoff_matrix = [[7,9,12],[10,6,7],[9,13,5]]
# cost_list = [6,3,5]

sophisticated_auction(epsilon,agents,payoff_matrix,cost_list)
#naive_auction(agents,payoff_matrix,cost_list)
