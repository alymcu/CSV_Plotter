# Define the input and output file paths
input_file_path = "LOG001.bin"
output_file_path = "out.CSV"
import time
import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np
i=0
j=0
ch1 = 0
ch2 = 0
ch3 = 0
ch4 = 0
ch5 = 0
ch6 = 0
ch7 = 0
ch8 = 0
ch9 = 0
ch10 = 0
ch11 = 0
ch12 = 0
# Open the input file in binary mode and the output file in write mode
with open(input_file_path, "rb") as input_file, open(output_file_path, "w") as output_file:
    # Read the content of the input file in binary format
    binary_data = input_file.read()
    # print(len(binary_data)/30)
    # Split the binary data into four-byte chunks
    # four_byte_chunks = [binary_data[i:i+4] for i in range(0, len(binary_data), 4)]
    thirty_byte_chunks = [binary_data[i:i+30] for i in range(0, len(binary_data) - (len(binary_data) % 30), 30)]
    # print(thirty_byte_chunks)
    # print(len(thirty_byte_chunks)-1)
    # print(thirty_byte_chunks[0])
    # Convert each four-byte chunk to its decimal ASCII representation
    decimal_values = []
    decimal_values.append("Counter,")
    decimal_values.append("CH1,")
    decimal_values.append("CH2,")
    decimal_values.append("CH3,")
    decimal_values.append("CH4,")
    decimal_values.append("CH5,")
    decimal_values.append("CH6,")
    decimal_values.append("CH7,")
    decimal_values.append("CH8,")
    decimal_values.append("CH9,")
    decimal_values.append("CH10,")
    decimal_values.append("CH11,")
    decimal_values.append("CH12")
    decimal_values.append("\n")


    # print(thirty_byte_chunks)
    counter_len = len(thirty_byte_chunks) - 1
    print(counter_len)
    for chunk in thirty_byte_chunks:
        if i == counter_len: break
        counting3, counting4, counting1, counting2, ch1l , ch1h, ch2l , ch2h, ch3l , ch3h, ch4l, ch4h, ch5l, ch5h, ch6l, ch6h, ch7l, ch7h, ch8l, ch8h, ch9l, ch9h, ch10l, ch10h, ch11l, ch11h, ch12l, ch12h , check1, check2 = chunk
        decimal_value = counting4 * 256**3 + counting3 * 256**2 + counting2 * 256 + counting1
        # print("Mem_Counter ", decimal_value, "    My Counter ", i+59)
        # if decimal_value != i+59:
        #     j = j + 1
        #     print("Counting Error ", j)
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch1h * 256 + ch1l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch2h * 256 + ch2l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch3h * 256 + ch3l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch4h * 256 + ch4l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch5h * 256 + ch5l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch6h * 256 + ch6l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch7h * 256 + ch7l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch8h * 256 + ch8l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch9h * 256 + ch9l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch10h * 256 + ch10l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch11h * 256 + ch11l
        decimal_values.append(str(decimal_value))
        decimal_values.append(",")
        decimal_value = ch12h * 256 + ch12l
        decimal_values.append(str(decimal_value))
        decimal_values.append("\n")
        # print(i)
        i = i + 1
    
    print("my val",counter_len)
    # for chunk in four_byte_chunks:
    #     byte1, byte2, byte3, byte4 = chunk
    #     decimal_value = byte1 * 256**3 + byte2 * 256**2 + byte3 * 256 + byte4
    #     decimal_values.append(str(decimal_value))

    # Write the decimal values to the output file
    output_file.write("".join(decimal_values))
    # print("writing CSV Completed...")
    time.sleep(1)

def autoscale_y(ax,margin=0.1):
    """This function rescales the y-axis based on the data that is visible given the current xlim of the axis.
    ax -- a matplotlib axes object
    margin -- the fraction of the total height of the y-data to pad the upper and lower ylims"""

    import numpy as np

    def get_bottom_top(line):
        xd = line.get_xdata()
        yd = line.get_ydata()
        lo,hi = ax.get_xlim()
        y_displayed = yd[((xd>lo) & (xd<hi))]
        h = np.max(y_displayed) - np.min(y_displayed)
        bot = np.min(y_displayed)-margin*h
        top = np.max(y_displayed)+margin*h
        return bot,top

    lines = ax.get_lines()
    bot,top = np.inf, -np.inf

    for line in lines:
        new_bot, new_top = get_bottom_top(line)
        if new_bot < bot: bot = new_bot
        if new_top > top: top = new_top

    ax.set_ylim(bot,top)


df = pd.read_csv(output_file_path)
df.plot(x="Counter", y=["CH1", "CH2" , 'CH3' , 'CH4',"CH5", 'CH6',"CH7", "CH8",'CH9','CH10','CH11','CH12'])
# df.plot(x="Counter", y=['CH10'])
# plt.xlim(30100, 30300)
# plt.axis('tight')
plt.show()