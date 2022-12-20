### Create animations visualizing citation network, downloaded as json file from VOSviewer.com

import json
from manim import *
from matplotlib import cm
from matplotlib.colors import rgb2hex
import numpy as np

### open JSON file of VOSviewer citation network
with open('VOSviewer-network.json', 'r') as f:
    vos = json.load(f)['network']
    nodes = vos['items']
    links = vos['links']

cmap = cm.get_cmap('viridis')
#config.background_color = WHITE



### create animation class for static citation network, inheriting from basic Scene Manim class
class CitationNetworkStatic(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-1.1,1.2], y_range=[-1.1,1.1], axis_config={"include_tip": False}
        )

        ### create link for each citation, add line to animation
        for link in links:
            source = [node for node in nodes if node['id'] == link['source_id']][0]
            target = [node for node in nodes if node['id'] == link['target_id']][0]
            line = Line(ax.coords_to_point(source['x'], source['y']), ax.coords_to_point(target['x'], target['y']), color=GREY)
            line.set_opacity(0.6)
            self.add(line)

        ### create circle for each node, colored by cluster and sized by citations. Create group for each cluster, labeled by largest node. add all circles to animation.
        nodegroups = []
        nodegrouplabels = []
        nodegroupweights = []
        for cluster in range(1, 50):
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
                circle.set_fill(color, opacity = 0.8)
                circle.move_to(ax.coords_to_point(node['x'], node['y']))
                circle.scale(np.log10(node['weights']['Citations']+2)/15)
                self.add(circle)
                nodegrouplist.append(circle)
            nodegroup = Group(*nodegrouplist)
            nodegroups.append(nodegroup)

        ### add text for central author in each cluster
        order = np.argsort(nodegroupweights)[::-1]
        for i in order:
            nodegroup = nodegroups[i]
            if len(nodegroup) > 0:
                text = Text(nodegrouplabels[i][0]).set_color(WHITE).move_to(nodegroup).scale(np.log10(nodegroupweights[i][0]+10) / 8)
                #.set(width = max(nodegroup.width*1.2, 1.0))
                self.add(text)




### create animation class for zooming citation network, inheriting from MovingCameraScene Manim class
class CitationNetworkAnimated(MovingCameraScene):
    def construct(self):
        ax = Axes(
            x_range=[-1.1,1.2], y_range=[-1.1,1.1], axis_config={"include_tip": False}
        )

        ### create link for each citation, add line to animation
        for link in links:
            source = [node for node in nodes if node['id'] == link['source_id']][0]
            target = [node for node in nodes if node['id'] == link['target_id']][0]
            line = Line(ax.coords_to_point(source['x'], source['y']), ax.coords_to_point(target['x'], target['y']), color=GREY)
            line.set_opacity(0.6)
            self.add(line)

        ### create circle for each node, colored by cluster and sized by citations. Create group for each cluster, labeled by largest node. add all circles to animation.
        self.wait(1)
        nodegroups = []
        nodegrouplabels = []
        nodegroupweights = []
        for cluster in range(1, 50):
            nodelist = [node for node in nodes if node['cluster'] == cluster]
            if len(nodelist) > 0:
                color =  rgb2hex(cmap(cluster/25))
                nodeweights = [node['weights']['Citations'] for node in nodelist]
                largestlabel = [node['label'] for node in nodelist if node['weights']['Citations'] == max(nodeweights)]
                largestweight = [node['weights']['Citations'] for node in nodelist if node['weights']['Citations'] == max(nodeweights)]
                nodegrouplabels.append(largestlabel)
                nodegroupweights.append(largestweight)
                nodegrouplist = []
                for node in nodelist:
                    circle = Circle(color = color)
                    circle.set_fill(color, opacity = 0.8)
                    circle.move_to(ax.coords_to_point(node['x'], node['y']))
                    circle.scale(np.log10(node['weights']['Citations']+2)/15)
                    self.add(circle)
                    nodegrouplist.append(circle)
                nodegroup = Group(*nodegrouplist)
                nodegroups.append(nodegroup)
                self.wait(0.25)

        ### now animate zooming & labeling clusters 1 by 1
        self.camera.frame.save_state()
        self.wait(1)
        order = np.argsort(nodegroupweights)[::-1]
        for i in order:
            nodegroup = nodegroups[i]
            if len(nodegroup) > 0:
                text = Text(nodegrouplabels[i][0]).set_color(WHITE).move_to(nodegroup).scale(np.log10(nodegroupweights[i][0]+10) / 8)
                #text = Text(nodegrouplabels[i][0]).set_color(WHITE).move_to(nodegroup).set(width = nodegroup.width*1.2)
                self.play(self.camera.frame.animate.move_to(nodegroup).set(width = max(nodegroup.width * 2, text.width * 2)))
                self.play(Rotate(nodegroup, angle=2*PI))
                self.add(text)
                self.wait(1)
                self.remove(text)
                self.play(Restore(self.camera.frame))





