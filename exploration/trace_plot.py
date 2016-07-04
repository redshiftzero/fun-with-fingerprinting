import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Disable warning on a value trying to be set on a copy of a slice of a df
pd.options.mode.chained_assignment = None

shape_dict = {
    'BEGIN_DIR(13)': 'D',
    'DATA(2)': 'H',
    'CONNECTED(4)': 's',
    'END(3)': 'v',
    'BEGIN(1)': 'o',
    'SENDME(5)': 'H',
    'EXTEND(6)': 'o',
    'EXTEND2(14)': 'H',
    'EXTENDED(7)': 'v',
    'EXTENDED2(15)': 'd',
    'ESTABLISH_RENDEZVOUS(33)': 'd',
    'RENDEZVOUS_ESTABLISHED(39)': 'D',
    'RENDEZVOUS2(37)': 'v',
    'INTRODUCE1(34)': 'H',
    'INTRODUCE_ACK(40)': 's'}

color_dict = {
    'BEGIN_DIR(13)': "#268bd2",
    'DATA(2)': "#586e75",
    'CONNECTED(4)': "#268bd2",
    'END(3)': "#268bd2",

    'BEGIN(1)': "#268bd2",
    'SENDME(5)': "#268bd2",

    'EXTEND(6)': "#cb4b16",
    'EXTEND2(14)': "#cb4b16",
    'EXTENDED(7)': "#cb4b16",
    'EXTENDED2(15)': "#cb4b16",

    'ESTABLISH_RENDEZVOUS(33)': "#2aa198",
    'RENDEZVOUS_ESTABLISHED(39)': "#2aa198",
    'RENDEZVOUS2(37)': "#2aa198",

    'INTRODUCE1(34)': "#859900",
    'INTRODUCE_ACK(40)': "#859900"}


def create_single(timeline, maximums=None, titlestr="", fig_height=16,
                  fig_width=20, marker_size=150.0):
    # Extract the data for plotting.
    if maximums is None:
        timeline['Elapsed'] = timeline['t_trace'] - timeline['t_trace'].iloc[0]
        maximums = timeline
    else:
        maximums['Elapsed'] = maximums['t_trace'] - maximums['t_trace'].iloc[0]
        timeline['Elapsed'] = timeline['t_trace'] - maximums['t_trace'].iloc[0]

    x_data = timeline['Elapsed']
    y_data = timeline['length']
    type_data = timeline['command']
    max_x = max(maximums['Elapsed'])
    max_y = max(maximums['length'])

    # Get a list of unique types in the timeline data.
    unique_types = list(type_data.unique())

    # Create a figure and time-axis.
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.hold(True)

    # For each event type, create a scatter plot.
    for event_type in unique_types:

        # Get the x and y values.i
        mask = timeline['command'] == event_type
        data = timeline[mask]
        x_data = data['Elapsed']
        y_data = data['length']

        # For light colors, make the edges darker.
        if color_dict[event_type] in ["yellow", "white", "pink"]:
            linewidth = 1.5
        else:
            linewidth = 0.0

        # Create the scatter plot.
        ax.scatter(x_data.values, y_data.values,
                   label=event_type.split('(')[0],
                   marker=shape_dict[event_type], s=marker_size,
                   c=color_dict[event_type],
                   linewidths=linewidth, alpha=0.80)

    # Make the figure pretty.
    fig.autofmt_xdate()
    ax.yaxis.set_visible(True)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.set_axis_bgcolor('whitesmoke')
    plt.xticks(rotation=80)
    plt.tick_params(labelsize=20)
    ax.set_xlabel('Elapsed Time (s)')
    ax.set_ylabel('Length (bytes)')
    ax.set_xlim([-0.25, max_x + 1])
    ax.set_ylim([-25, max_y + 200])

    handles, labels = ax.get_legend_handles_labels()

    # or sort them by labels
    import operator
    hl = sorted(zip(handles, labels),
                key=operator.itemgetter(1))
    handles2, labels2 = zip(*hl)

    ax.legend(handles2, labels2, loc=2, numpoints=1, scatterpoints=1)

    # Remove grid lines
    ax.grid(False)
    # Remove plot frame
    ax.set_frame_on(False)
    # Set the title.
    plt.title(titlestr, fontsize=20)

    # Show the plot.
    plt.show()

    # Return the axis handle.
    return None


def create_by_circuit(df, titlestr):
    for circuit in df['circuit'].unique():
        df_circuit = df[df['circuit'] == circuit]
        create_single(df_circuit, maximums=df,
                      titlestr="Trace {}: Tor Circuit {}".format(titlestr,
                                                                 circuit))
    return None
