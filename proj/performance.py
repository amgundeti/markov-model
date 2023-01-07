import sys
from markov import identify_speaker
import pandas
import time
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)


    fileA = open(f"proj/{filenameA}", "r").read()
    fileB = open(f"proj/{filenameB}", "r").read()
    fileC = open(f"proj/{filenameC}", "r").read()

    #dictionary for recording values as for loop executes - converted into pandas dataframe later
    d = {"Implementation": [], "k": [ ], "Run": [ ], "Time": [ ]}

    for i in range(max_k+1):
        for j in range(1,runs+1):
            start_h = time.perf_counter()
            actual = identify_speaker(fileA, fileB, fileC, i, True)
            elapsed_h = time.perf_counter() - start_h

            #appending information to dict for hashtable run
            d["Implementation"].append("Hashtable")
            d["k"].append(i)
            d["Run"].append(j)
            d["Time"].append(elapsed_h)

            start_d = time.perf_counter()
            actual = identify_speaker(fileA, fileB, fileC, i, False)
            elapsed_d = time.perf_counter() - start_d

            #appending information to dict for dict run
            d["Implementation"].append("Dict")
            d["k"].append(i)
            d["Run"].append(j)
            d["Time"].append(elapsed_d)

    #creating data frame from dict and grouping by k and implementation
    df = pandas.DataFrame(d)
    df1 = df.groupby(by=["k", "Implementation"]).mean()

    sns.set_theme()

    ax = sns.lineplot(
        data=df1, x="k", y="Time",
        color=".7", linewidth=1, markers=True, legend="full", hue="Implementation",
        marker="o"
    )

    ylabel_r = f"Time (Seconds) - Average of {runs} Runs"
    ax.set_title("K Order Markov Model - Python Dict vs. Hashtable")
    ax.set(xlabel='K Order', ylabel=ylabel_r)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))


    plt.savefig("performance.png")