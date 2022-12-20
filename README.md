# citation_networks_manim
Playing around with Manim Python library to create animated visualizations of citation networks.

See [docs](https://docs.manim.community/en/v0.15.2/index.html) for installation instructions and examples, plus this [TowardsDataScience](https://towardsdatascience.com/how-to-create-mathematical-animations-like-3blue1brown-using-python-f571fb9da3d1) post for more helpful examples.

Run ``make_scene_vosviewer.sh`` to create citation network animation. This will create a gif in the ``media`` directory. 
The input data ``VOSviewer-network.json`` was created using the Dimensions and VOSviewer tools, as outlined in [this blogpost](https://waterprogramming.wordpress.com/2022/07/05/viewing-your-scientific-landscape-with-vosviewer/) by Rohini Gupta. The JSON file was downloaded from the [Reed Group website](https://reed.cee.cornell.edu/software/) by clicking "save" in the interactive VOSviewer application.


