    // State Machine manipulating functions called from the controller
    PetriVizWidget.prototype.initMachine = function (machineDescriptor) {
        const self = this;
        console.log(machineDescriptor);

        self._webgmePN = machineDescriptor;
        self._webgmePN.current = self._webgmePN.init;
        self._jointPN.clear();
        const pn = self._webgmePN;
        pn.id2place = {}; // this dictionary will connect the on-screen id to the state id
        // first add the places
        Object.keys(pn.places).forEach(placeID => {
            let vertex = null;
            if (pn.init === placeID) {
                vertex = new joint.shapes.standard.Circle({
                    position: pn.places[placeID].position,
                    size: { width: 20, height: 20 },
                    attrs: {
                        body: {
                            fill: '#333333',
                            cursor: 'pointer'
                        }
                    }
                });
            } else if (pn.places[placeID].isEnd) {
                vertex = new joint.shapes.standard.Circle({
                    position: sm.places[placeID].position,
                    size: { width: 30, height: 30 },
                    attrs: {
                        body: {
                            fill: '#999999',
                            cursor: 'pointer'
                        }
                    }
                });
            } else {
                vertex = new joint.shapes.standard.Circle({
                    position: pn.places[placeID].position,
                    size: { width: 60, height: 60 },
                    attrs: {
                        label : {
                            text: pn.places[placeID].name,
                            //event: 'element:label:pointerdown',
                            fontWeight: 'bold',
                            //cursor: 'text',
                            //style: {
                            //    userSelect: 'text'
                            //}
                        },
                        body: {
                            strokeWidth: 3,
                            cursor: 'pointer'
                        }
                    }
                });
            }
            vertex.addTo(self._jointPN);
            pn.places[placeID].joint = vertex;
       //     pn.id2state[vertex.id] = placeID;
        });

        // then create the links
        Object.keys(pn.places).forEach(placeID => {
            const place = pn.places[placeID];
            Object.keys(place.next).forEach(event => {
                place.jointNext = place.jointNext || {};
                const link = new joint.shapes.standard.Link({
                    source: {id: place.joint.id},
                    target: {id: pn.places[place.next[event]].joint.id},
                    attrs: {
                        line: {
                            strokeWidth: 2
                        },
                        wrapper: {
                            cursor: 'default'
                        }
                    },
                    labels: [{
                        position: {
                            distance: 0.5,
                            offset: 0,
                            args: {
                                keepGradient: true,
                                ensureLegibility: true
                            }
                        },
                        attrs: {
                            text: {
                                text: event,
                                fontWeight: 'bold'
                            }
                        }
                    }]
                });
                link.addTo(self._jointPN);
                place.jointNext[event] = link;
            })
        });