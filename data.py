import matplotlib.pyplot as plt
import pandas as pd

def ploting (l1,l2,l3, maxRuns, agentNum):
    x = [i for i in range(maxRuns)]
    y = l1
    plt.plot(x, y, marker='o', color='b',label='success_rate')
    plt.xticks(x)
    # for i, j in zip(x, y)
    #     plt.text(i, j + 0.005, "({}, {})".format(i, round(j, 2)))
    y = l2
    plt.plot(x, y, marker='o', color='r',label='failure_rate_predator')

    y = l3
    plt.plot(x, y, marker='o', color='b',label='timeout_rate')
    plt.xlabel('Number of Runs')
    plt.ylabel('Average Rate')
    plt.title("AGENT {} (Tested on {} graphs for each run)".format(agentNum, len(l1)))
    plt.show()


agent_success = []
failure_pred = []
failure_timeout = []

agentNum = int(input("Enter the agent number: "))
maxRuns = int(input("Enter the max number of ghosts that you want to cram data for: "))


for i in range(maxRuns):
    filepath = "./agent_csv/agent" + str(agentNum) + "/Run" + str(i) + '.csv'
    df = pd.read_csv(filepath)
    success_rate = df["success"].mean()
    agent_success.append(success_rate)
    failure_rate = df["failure_predator"].mean()
    failure_pred.append(success_rate)
    timeout_rate = df["Failure_Timeout"].mean()
    failure_timeout.append(success_rate)

    
ploting(agent_success,failure_pred,failure_timeout,maxRuns,agentNum)