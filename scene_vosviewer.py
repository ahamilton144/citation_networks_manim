### Now create animations visualizing citation network, downloaded as json file from VOSviewer.com

import json
from manim import *
from matplotlib import cm
from matplotlib.colors import rgb2hex
import numpy as np
from numpy import array

with open('VOSviewer-network.json', 'r') as f:
    vos = json.load(f)['network']
    nodes = vos['items']
    links = vos['links']
print(nodes[0])
print(links[0])
cmap = cm.get_cmap('viridis')
config.background_color = WHITE

class CitationNetwork(Scene):

    def construct(self):
        ax = Axes(
            x_range=[-1.1,1.2], y_range=[-1.1,1.1], axis_config={"include_tip": False}
        )

        for cluster in range(1, 25):
            nodelist = [node for node in nodes if node['cluster'] == cluster]
            color =  rgb2hex(cmap(cluster/25))
            for node in nodelist:
                circle = Circle(color = color)
                circle.set_fill(color, opacity = 0.5)
                circle.move_to(ax.coords_to_point(node['x'], node['y']))
                circle.scale(node['scores']['Avg. norm. citations']/10)
                self.add(circle)
            self.wait(0.5)


class CitationNetworkZoom(MovingCameraScene):

    def construct(self):
        ax = Axes(
            x_range=[-1.1,1.2], y_range=[-1.1,1.1], axis_config={"include_tip": False}
        )

        ### create link for each citation
        for link in links:
            source = [node for node in nodes if node['id'] == link['source_id']][0]
            target = [node for node in nodes if node['id'] == link['target_id']][0]
            line = Line(ax.coords_to_point(source['x'], source['y']), ax.coords_to_point(target['x'], target['y']), color=GREY)
            line.set_opacity(0.3)
            self.add(line)

        ### create circle for each node, colored by cluster and sized by citations. Create group for each cluster, labeled by largest node.
        nodegroups = []
        nodegrouplabels = []
        nodegroupweights = []
        for cluster in range(1, 25):
            nodelist = [node for node in nodes if node['cluster'] == cluster]
            color =  rgb2hex(cmap(cluster/25))
            nodeweights = [node['weights']['Citations'] for node in nodelist]
            largestlabel = [node['label'] for node in nodelist if node['weights']['Citations'] == max(nodeweights)]
            largestweight = [node['weights']['Citations'] for node in nodelist if node['weights']['Citations'] == max(nodeweights)]
            nodegrouplabels.append(largestlabel)
            nodegroupweights.append(largestweight)
            nodegrouplist = []
            for node in nodelist:
                circle = Circle(color = color)
                circle.set_fill(color, opacity = 0.7)
                circle.move_to(ax.coords_to_point(node['x'], node['y']))
                circle.scale(np.log10(node['weights']['Citations']+2)/15)
                self.add(circle)
                nodegrouplist.append(circle)
            nodegroup = Group(*nodegrouplist)
            nodegroups.append(nodegroup)

        ### now animate zooming & labeling clusters 1 by 1
        self.camera.frame.save_state()
        self.wait(1)
        order = np.argsort(nodegroupweights)[::-1]
        for i in order:
            nodegroup = nodegroups[i]
            if len(nodegroup) > 0:
                self.play(self.camera.frame.animate.move_to(nodegroup).set(width = nodegroup.width * 2))
                text = Text(nodegrouplabels[i][0]).set_color(BLACK).move_to(nodegroup).set(width = nodegroup.width*1.2)
                self.play(Rotate(nodegroup, angle=2*PI))
                self.add(text)
                self.wait(1)
                self.remove(text)
                self.play(Restore(self.camera.frame))



