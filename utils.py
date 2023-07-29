
__author__ = "Hari Krishna Veerala"
__credits__ = ["", ""]
__license__ = ""
__version__ = "1.0.1"
__maintainer__ = ""
__email__ = "veeralakrishna.com"
__status__ = "Development" # Production/Development


VERSION = "0.2.2"
#---------------------------------------------------------------------------
#                                imports
#---------------------------------------------------------------------------


import os
import json
import numpy as np
import matplotlib.cm as cm

import plotly.graph_objs as go


from pathlib import Path
from functools import reduce
from operator import itemgetter
from plyfile import PlyData, PlyElement

import streamlit as st

#---------------------------------------------------------------------------
#                                Viz-Utils
#---------------------------------------------------------------------------

def tri_indices(simplices):
    """
    params:
        simplices is a numpy array defining the simplices of the triangularization
        
    return:
        returns the lists of indices i, j, k
    """
    
    return ([triplet[c] for triplet in simplices] for c in range(3))

def plotly_trisurf(x, y, z, simplices, colormap=cm.RdBu, plot_edges=None):
    """
    x, y, z are lists of coordinates of the triangle vertices 
    simplices are the simplices that define the triangularization;
    simplices  is a numpy array of shape (no_triangles, 3)
    """

    points3D=np.vstack((x,y,z)).T
    tri_vertices=map(lambda index: points3D[index], simplices)
    zmean=[np.mean(tri[:,2]) for tri in tri_vertices ]
    min_zmean=np.min(zmean)
    max_zmean=np.max(zmean)
    facecolor=[map_z2color(zz,  
                           colormap, 
                           min_zmean, 
                           max_zmean) for zz in zmean]
    I,J,K=tri_indices(simplices)

    triangles=go.Mesh3d(x=x, 
                        y=y, 
                        z=z,
                        facecolor=facecolor,
                        i=I, 
                        j=J, 
                        k=K,
                        name='')

    if plot_edges is None: return [triangles]
    else:
        lists_coord=[[[T[k%3][c] for k in range(4)]+[ None]   for T in tri_vertices]  for c in range(3)]
        Xe, Ye, Ze = [reduce(lambda x,y: x+y, lists_coord[k]) for k in range(3)]

        lines=go.Scatter3d(x=Xe, 
                           y=Ye, 
                           z=Ze,
                           mode='lines',
                           line=dict(color='rgb(50,50,50)', 
                                     width=1.5))
        return [triangles, lines]

    
def map_z2color(zval, colormap, vmin, vmax):
    """
    map the normalized value zval to a corresponding color in the colormap
    """
    if vmin>vmax: 
        raise ValueError('incorrect relation between vmin and vmax')
        
    t=(zval-vmin)/float((vmax-vmin))#normalize val
    R, G, B, alpha=colormap(t)
    
    return 'rgb('+'{:d}'.format(int(R*255+0.5))+','+'{:d}'.format(int(G*255+0.5))+\
           ','+'{:d}'.format(int(B*255+0.5))+')'
           
           


def plotly_Surface_Triangulation(file_name,
                                 data_type,
                                 axis=True,
                                 paper_bgcolor='snow',
                                 width=900,
                                 height=500,
                                 save_html=None
                                 ):


    if data_type not in (".json", ".ply"):
        print(f"{file_name} - doesn't support")

    else:

        if data_type == ".json":

            with open(f"data/car_models_json/{file_name}.json") as json_file:
                # load json file
                data = json.load(json_file)
                # Extract vertices & triangles
                vertices, triangles = np.array(data['vertices']), np.array(data['faces']) - 1
                # Unpack vertices
                x, y, z = vertices[:,0], vertices[:,2], -vertices[:,1]
                # Get Car type from json
                car_type = data['car_type']

                file_name = file_name +  " - " + car_type

        elif data_type == ".ply":
            # req = urllib2.Request('https://people.sc.fsu.edu/~jburkardt/data/ply/skull.ply')
            # opener = urllib2.build_opener()
            # f = opener.open(req)
            plydata = PlyData.read(f"data/ply_data/{file_name}.ply")

            nr_points = plydata.elements[0].count
            nr_faces = plydata.elements[1].count
            points = np.array([plydata['vertex'][k] for k in range(nr_points)])

            if len(points[0]) > 3:
                points = list(map(itemgetter(0, 1, 2), points))

            x,y,z = zip(*points)
            triangles = [plydata['face'][k][0] for k in range(nr_faces)]


        # get Graph data
        graph_data = plotly_trisurf(x,
                                    y,
                                    z,
                                    triangles,
                                    colormap=cm.RdBu,
                                    plot_edges=None)

        if axis:
            # with axis
            axis = dict(
                showbackground=True,
                backgroundcolor="rgb(230, 230,230)",
                gridcolor="rgb(255, 255, 255)",
                zerolinecolor="rgb(255, 255, 255)",
            )

            scene=dict(
                xaxis=dict(axis),
                yaxis=dict(axis),
                zaxis=dict(axis),
                # aspectratio=dict( x=1, y=2, z=0.5),
                # camera=dict(eye=dict(x=1.25, y=1.25, z= 1.25))
             )

        else:
            # with no axis
            noaxis=dict(
                showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title=''
            )

            scene=dict(
                xaxis=dict(noaxis),
                yaxis=dict(noaxis),
                zaxis=dict(noaxis),

                 )

        layout = go.Layout(
            title= dict(
                text=file_name,
                x=0.5,
                y=0.95,
                font=dict(
                    family="Rockwell",
                    size=20,
                    color='#000000'
                    )
                ),
            hoverlabel=dict(
                bgcolor="rgba(58, 71, 80, 0.1)",
                font_size=16,
                font_family="Rockwell"
                ),
            margin=dict(
                l=0,
                b=0,
                r=0,
                t=0,
            ),
            width=width,
            height=height,

            paper_bgcolor=paper_bgcolor,
            scene=scene,
            scene_aspectmode="data"

    )


        fig = go.Figure(data=graph_data,
                        layout=layout)
        if save_html:
            fig.write_html(f"Output/{plotly_Surface_Triangulation}.html")
            
        # fig.show()
        st.plotly_chart(fig, use_container_width=True)
        


paper_bgcolr = ['aliceblue',
                'antiquewhite',
                'aqua',
                'aquamarine',
                'azure',
                'beige',
                'bisque',
                'black',
                'blanchedalmond',
                'blue',
                'blueviolet',
                'brown',
                'burlywood',
                'cadetblue',
                'chartreuse',
                'chocolate',
                'coral',
                'cornflowerblue',
                'cornsilk',
                'crimson',
                'cyan',
                'darkblue',
                'darkcyan',
                'darkgoldenrod',
                'darkgray',
                'darkgrey',
                'darkgreen',
                'darkkhaki',
                'darkmagenta',
                'darkolivegreen',
                'darkorange',
                'darkorchid',
                'darkred',
                'darksalmon',
                'darkseagreen',
                'darkslateblue',
                'darkslategray',
                'darkslategrey',
                'darkturquoise',
                'darkviolet',
                'deeppink',
                'deepskyblue',
                'dimgray',
                'dimgrey',
                'dodgerblue',
                'firebrick',
                'floralwhite',
                'forestgreen',
                'fuchsia',
                'gainsboro',
                'ghostwhite',
                'gold',
                'goldenrod',
                'gray',
                'grey',
                'green',
                'greenyellow',
                'honeydew',
                'hotpink',
                'indianred',
                'indigo',
                'ivory',
                'khaki',
                'lavender',
                'lavenderblush',
                'lawngreen',
                'lemonchiffon',
                'lightblue',
                'lightcoral',
                'lightcyan',
                'lightgoldenrodyellow',
                'lightgray',
                'lightgrey',
                'lightgreen',
                'lightpink',
                'lightsalmon',
                'lightseagreen',
                'lightskyblue',
                'lightslategray',
                'lightslategrey',
                'lightsteelblue',
                'lightyellow',
                'lime',
                'limegreen',
                'linen',
                'magenta',
                'maroon',
                'mediumaquamarine',
                'mediumblue',
                'mediumorchid',
                'mediumpurple',
                'mediumseagreen',
                'mediumslateblue',
                'mediumspringgreen',
                'mediumturquoise',
                'mediumvioletred',
                'midnightblue',
                'mintcream',
                'mistyrose',
                'moccasin',
                'navajowhite',
                'navy',
                'oldlace',
                'olive',
                'olivedrab',
                'orange',
                'orangered',
                'orchid',
                'palegoldenrod',
                'palegreen',
                'paleturquoise',
                'palevioletred',
                'papayawhip',
                'peachpuff',
                'peru',
                'pink',
                'plum',
                'powderblue',
                'purple',
                'red',
                'rosybrown',
                'royalblue',
                'rebeccapurple',
                'saddlebrown',
                'salmon',
                'sandybrown',
                'seagreen',
                'seashell',
                'sienna',
                'silver',
                'skyblue',
                'slateblue',
                'slategray',
                'slategrey',
                'snow',
                'springgreen',
                'steelblue',
                'tan',
                'teal',
                'thistle',
                'tomato',
                'turquoise',
                'violet',
                'wheat',
                'white',
                'whitesmoke',
                'yellow',
                'yellowgreen']