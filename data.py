import matplotlib.pyplot as plt
import pandas as pd

def plotting(l1, l2, l3, num_runs, num_trials, agent_num):

    # X
    x = [i for i in range(num_runs)]
    plt.xticks(x)

    # Plots for success/failure rates
    plt.plot(x, l1, marker='o', color='b', label='success_rate')
    plt.plot(x, l2, marker='o', color='r', label='failure_rate_predator')
    plt.plot(x, l3, marker='o', color='y', label='timeout_rate')

    # Labels and legend
    plt.xlabel('Run Numbers')
    plt.ylabel('Average Rate')
    plt.title("AGENT {} (Tested on {} trials for each run)".format(agent_num, num_trials))
    plt.legend()

    # Just save a PNG for the plot
    plt.gcf().set_size_inches(11.2775330396, 7.04845814978) # The MacbookPro 13.3 inches size
    plt.savefig("./graphs/agent{}.png".format(agent_num), dpi=227) # The MacbookPro 13.3 inches dpi

agent_num = int(input("Enter the agent number: "))
num_runs = int(input("Enter the number of runs for which you want to cram data: "))

agent_success = []
failure_pred = []
failure_timeout = []
num_trials = 0

for run in range(num_runs):
    filepath = "./agent_csv/agent" + str(agent_num) + "/Run" + str(run) + '.csv'
    df = pd.read_csv(filepath)
    success_rate = df["success"].mean()
    agent_success.append(success_rate)
    failure_rate = df["failure_predator"].mean()
    failure_pred.append(failure_rate)
    timeout_rate = df["failure_timeout"].mean()
    failure_timeout.append(timeout_rate)

    if num_trials == 0:
        num_trials = len(df)
    
plotting(agent_success, failure_pred, failure_timeout, num_runs, num_trials, agent_num)