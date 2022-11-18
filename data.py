import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import statistics

def plotting(l1, l2, l3, num_runs, num_trials, agent_num, agent_char):

    # X
    x = [i for i in range(num_runs)]
    plt.xticks(x)

    # Plots for success/failure rates
    plt.plot(x, l1, marker='o', color='b', label='success_rate')
    for i, j in zip([x[i] for i in range(0,len(x),5)],[l1[i] for i in range(0,len(l1),5)] ):
        plt.text(i+ 0.050, j + 0.0010, "({}, {})".format(i, round(j, 2)))

    plt.plot(x, l2, marker='o', color='r', label='failure_rate_predator')
    for i, j in zip([x[i] for i in range(0,len(x),5)],[l2[i] for i in range(0,len(l2),5)] ):
        plt.text(i+ 0.050, j + 0.010, "({}, {})".format(i, round(j, 2)))

    plt.plot(x, l3, marker='o', color='y', label='timeout_rate')
    for i, j in zip([x[i] for i in range(0,len(x),5)],[l3[i] for i in range(0,len(l3),5)] ):
        plt.text(i+ 0.050, j + 0.010, "({},{})".format(i, round(j, 2)))

    # Labels and legend
    plt.xlabel('Run Numbers')
    plt.ylabel('Average Rate')
    plt.title("AGENT {} (Tested on {} trials for each run)".format(agent_num, num_trials))
    plt.legend()
    

    # Just save a PNG for the plot
    plt.gcf().set_size_inches(11.2775330396, 7.04845814978) # The MacbookPro 13.3 inches size
    plt.savefig("./graphs/agent{}.png".format(str(agent_num) + agent_char), dpi=227) # The MacbookPro 13.3 inches dpi
    plt.show()

def plotting2(l1, l2, num_runs, num_trials, agent_num, agent_char):

    # X
    x = [i for i in range(num_runs)]
    plt.xticks(x)

    # Plots for success/failure rates
    plt.plot(x, l1, marker='o', color='b', label='prey_known_rate')
    for i, j in zip([x[i] for i in range(0,len(x),5)],[l1[i] for i in range(0,len(l1),5)] ):
        plt.text(i+ 0.050, j + 0.0010, "({}, {})".format(i, round(j, 2)))

    plt.plot(x, l2, marker='o', color='r', label='predator_known_rate')
    for i, j in zip([x[i] for i in range(0,len(x),5)],[l2[i] for i in range(0,len(l2),5)] ):
        plt.text(i+ 0.050, j + 0.010, "({}, {})".format(i, round(j, 2)))

    # Labels and legend
    plt.legend(loc="upper right")
    plt.xlabel('Run Numbers')
    plt.ylabel('accurate_prediction')
    plt.title("AGENT {} (Tested on {} trials for each run)".format(agent_num, num_trials))
    plt.legend()
    

    # Just save a PNG for the plot
    plt.gcf().set_size_inches(11.2775330396, 7.04845814978) # The MacbookPro 13.3 inches size
    plt.savefig("./know_graphs/agent{}.png".format(str(agent_num) + agent_char), dpi=227) # The MacbookPro 13.3 inches dpi
    plt.show()
    plt.show()

def weighted_avg_and_std(values, weights):

    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)

    return (average, math.sqrt(variance))


agent_num = int(input("Enter the agent number: "))

agent_char = ""
if agent_num == 7 or agent_num == 8:
    agent_char = str(input("Enter a space if normal agent 7 or 8, else enter b: ")).strip()

num_runs = 30
# int(input("Enter the number of runs for which you want to cram data: "))

agent_success = []
failure_pred = []
failure_timeout = []
num_trials = 0

prey_known = []
pred_known = []
total_timesteps_run = []


for run in range(num_runs):
    filepath = "./agent_csv/agent" + str(agent_num) + agent_char + "/Run" + str(run) + '.csv'
    df = pd.read_csv(filepath)
    success_rate = df["success"].mean()
    agent_success.append(success_rate)
    failure_rate = df["failure_predator"].mean()
    failure_pred.append(failure_rate)
    timeout_rate = df["failure_timeout"].mean()
    failure_timeout.append(timeout_rate)

    filepath2 = "./know_csv/agent" + str(agent_num) + agent_char + "/Run" + str(run) + '.csv'
    df2 = pd.read_csv(filepath2)
    prey_known_percentage = df2['times_prey_known'].sum()*100/df2['time_steps'].sum()
    prey_known.append(prey_known_percentage)
    pred_known_percentage = df2['times_pred_known'].sum()*100/df2['time_steps'].sum()
    pred_known.append(pred_known_percentage)
    total_timesteps = df2['time_steps'].mean()
    total_timesteps_run.append(total_timesteps)

    if num_trials == 0:
        num_trials = len(df)


mean_success = sum(agent_success)*100/len(agent_success)
sd_success = statistics.pstdev(agent_success)*100

mean_failure_predator = sum(failure_pred)*100/len(failure_pred)
sd_failure_predator = statistics.pstdev(failure_pred)*100

mean_failure_timeout = sum(failure_timeout)*100/len(failure_timeout)
sd_failure_timeout = statistics.pstdev(failure_timeout)*100

mean_prey , sd_prey = weighted_avg_and_std(prey_known, total_timesteps_run)
mean_pred , sd_pred = weighted_avg_and_std(pred_known, total_timesteps_run)

mean__t_ts = sum(total_timesteps_run)/len(total_timesteps_run)
sd_t_ts = statistics.pstdev(total_timesteps_run)

df = pd.DataFrame()
df["success"]= [mean_success,sd_success]
df["failure_predator"]= [mean_failure_predator,sd_failure_predator]
df["failure_timeout"]= [mean_failure_timeout,sd_failure_timeout]
df["Prey_know"] = [mean_prey,sd_prey]
df["Predator_known"] = [mean_pred,sd_pred]
df["Average_Timesteps"] = [mean__t_ts,sd_t_ts]

file_name = "./final/agent" + str(agent_num) + agent_char + '.csv'
df.to_csv(file_name, encoding='utf-8')

plotting(agent_success, failure_pred, failure_timeout, num_runs, num_trials, agent_num, agent_char)
plotting2(prey_known,pred_known, num_runs, num_trials, agent_num, agent_char)
