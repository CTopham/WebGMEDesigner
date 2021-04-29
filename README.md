# Craig Topham MiniProject
## Model Integrated Computing


## Model and Domain Information
- What is the domain about

    The domain is a petri net which allows the user to set a required marker count in order to succesfully fire. The importannce of such a domain could allow for better views into semantics controls in systems which require barrier synchronization. The domain meta model contains states such as 'places' and and transitions. The linkage inherit from 'arks'. The Arks are delineated into 2 categories depending if 
    they are coming a transition or a place.

- A few sentence on the typical use-cases of the domain

    For a typical use case I believe an example would best start the imagination. The scenario is you working at a golf club manufacturing plant as the lead engineer to make the world best 9 iron! Your idea is have the machinery weld together the pieces of the golf club at the more optimized moment, when the shaft is at the hottest temperature. In order to accomplish this you will need to model your strategy. You do this by using a petri net! In the model you set up 3 places, one for each triangluar point on the shaft of the club. You find that the club is best heated when you dab the machines torch against the shaft top point 4 times the left point 2 times and the right point 2 times. The model can be demonstrated in the petri net by 3 places, one for each point in the shaft, in those places the markers will correspond to every torch dab against its target. The running result of the model will display how to heat up the golf clubs shaft at the best time and sequence to build the strongest golf club the universe has every seen.


- How to install the design studio

- - First, install the MiniProjectA following:
- - [NodeJS](https://nodejs.org/en/) (LTS recommended)
- - [MongoDB](https://www.mongodb.com/)

- - Second, start mongodb locally by running the `mongod` executable in your mongodb installation (you may need to create a `data` directory or set `--dbpath`).

Then, run `webgme start` from the project root to start . Finally, navigate to `http://localhost:8888` to start using MiniProjectA!

- How to start modeling once the studio is installed
    Once the model is built you will be able to select the 'composition' view at the root level on the top left corner of the screen, under the visualizer list. In this list you will see a document icon that says 'petri'. Drag that onto the workspace in the center of the screen then double click it. You will now be in a blank workspace, on the left side you will see all the nodes you can use as building blocks to build your domain specific language. Start with a 'place' then add transitions between additional places. Then connect your places with arks by dragging the cursor from one place to the next. Lastly set your markers up by double clicking a place and dragging over the set amount of makers you would like the intial state of the place to have.

- Once a network is build, what feature your studio provides and how can the user use
those functions

    The Design studion will provide a robust interpreter to help clarify what type of petri net you build. This will help to identify if your petri net conforms to the type of model you are attempting to make. If you click the 'road' button in the top left side of the tool bar you will notice notifications that will begin popping up on the bottom right side of the screen. These notifications will a a variation of the following: 
    NOT a free choice petri net
            - Free Choice Petri Net
            - StateMachine Petri Net
            - NOT a StateMachine Petri Net'
            - Marked Graph Petri Net
            - NOT a Marked Graph Petri Net