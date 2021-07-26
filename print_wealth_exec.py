import pandas as pd
import plotly.express as px


def main():
    data = pd.read_csv("raw/wealth_history_execution.csv")
    agents = data.iloc[:, 1].values
    columns = ["agent", "round", "wealth"]
    reduced_data = pd.DataFrame({"agent": [], "round": [], "wealth": []})
    aux_mtx = []

    print(agents)

    for agent_index in range(len(agents)):
        for round in range(2, data.shape[1]-1):
            aux_mtx.append([agents[agent_index], round, data.iloc[agent_index, round]])

    aux_data = pd.DataFrame(aux_mtx, columns=columns)

    for agent in agents:
        reduced_data = reduced_data.append(aux_data.loc[aux_data['agent'] == agent].loc[aux_data['round'] % 10 == 0])

    fig = px.bar(reduced_data, y='agent', x="wealth", animation_frame="round",
                  animation_group="agent", range_x=[0, 4500], orientation='h')

    fig.show()


main()
