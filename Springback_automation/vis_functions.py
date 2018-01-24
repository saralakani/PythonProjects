import pandas as pd
import os
from math import ceil
import plotly as py
from plotly.graph_objs import Scatter3d, Layout, Figure
def result_files(topdir):
    flist=[]
    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            flist.append(os.path.join(dirpath, name))
    return flist

def get_Scatter_plot(dframe):
    #these strings e.g. x-coor , x-disp are coming from the dumped csv file
    #which in turn is coming from the DYNA nodout file
    xt="x-coor"
    yt="y-coor"
    zt="z-coor"
    abs_disp=(dframe['x-disp']**2+dframe['y-disp']**2+dframe['z-disp']**2)**(0.5)
    axis_range=set_axis_ranges(dframe)
    trace=Scatter3d(x=dframe[xt].values,y=dframe[yt].values,z=dframe[zt].values,
    mode='markers',
    marker=dict(size=3,color=abs_disp,colorscale='Jet',showscale=True),
    legendgroup=abs_disp,
    hovertext=abs_disp)
    #data=[trace]
    layout=Layout(scene=dict(xaxis=dict(range=axis_range[xt]),
    yaxis=dict(range=axis_range[yt]),
    zaxis=dict(range=axis_range[zt])),
    margin=dict(l=0,r=0,b=0,t=0))
    #fig=Figure(data=data,layout=layout)
    return trace, layout
#returns a dictionary with the range values as lists [min,max]
def set_axis_ranges(dframe):
    #the keys for the dictionary which is the same as the dataframe column labels
    #which in turn is the same as
    axes=['x-coor','y-coor','z-coor']
    max_range=0
    axis_range={}
    for axis in axes:
        _range=dframe.max()[axis]-dframe.min()[axis]
        if _range > max_range:
            max_range = _range
    for axis in axes:
        center=(dframe.min()[axis]+dframe.max()[axis])/2
        lower=int(center-max_range/2)-1
        upper=int(center+max_range/2)+1
        axis_range[axis]=[lower,upper]
    return axis_range
#determine the number of rows and columns based on the number of objects
#it's based on an arbitrary scheme
def get_array_layout(number_of_objs):
    r=0
    c=0
    if number_of_objs==1:
        c=1
        r=1
    elif number_of_objs >= 2 and number_of_objs <= 4:
        c=2
        r=ceil(number_of_objs/2)
    elif number_of_objs > 4 and number_of_objs <=9:
        c=3
        r=ceil(number_of_objs/3)
    elif number_of_objs > 9:
        c=4
        r=ceil(number_of_objs/4)
    rc={"row_number":r,"col_number":c}
    return rc

#generates the subplot specs list according to plotly 2.0.7 standard
def gen_3d_specs(number_of_objs):
    a=[]
    rows=get_array_layout(number_of_objs)["row_number"]
    cols=get_array_layout(number_of_objs)["col_number"]
    spec={'is_3d': True}
    for i in range(rows):
        b=[]
        for j in range(cols):
            b.append(spec)
        a.append(b)
    return a
#data is the list of trace objects
def gen_sub_plots(data):
    number_of_objs=len(data)
    rc=get_array_layout(number_of_objs)
    fig=py.tools.make_subplots(rows=rc["row_number"],cols=rc["col_number"],
    specs=gen_3d_specs(number_of_objs))
    counter=1
    for i in range(rc["row_number"]):
        for j in range(rc["col_number"]):
            if counter <= number_of_objs:
                fig.append_trace(data[counter],i+1,j+1)
            counter+=1
    return fig

df=pd.read_csv(r'C:\Hamed\test.csv')
t, l=get_Scatter_plot(df)
data=[t,t,t,t]
fig=gen_sub_plots(data)
#fig=get_Scatter_plot(df)
py.offline.plot(fig,filename='test.html')
#print(get_array_layout(12))
#print(gen_3d_specs(12))
