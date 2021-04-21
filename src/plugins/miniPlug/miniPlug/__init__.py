"""
This is where the implementation of the plugin code goes.
The miniPlug-class is imported from both run_plugin.py and run_debug.py
"""
import sys
import logging
from webgme_bindings import PluginBase

# Setup a logger
logger = logging.getLogger('miniPlug')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)  # By default it logs to stderr..
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class miniPlug(PluginBase):
  def main(self):
    active_node = self.active_node
    core = self.core
    logger = self.logger
    nodes = core.load_sub_tree(active_node) # loads all nodes in our given model
    import json
    
    D = {}
    ingress = []
    egress = []
    allplaces = set()

    
    def traveler(node):
      temp = {}
      att = {}
      meta_node = core.get_base_type(node) # gets base node, in meta model
      name = core.get_attribute(node, 'name') # get the given node name
      path = core.get_path(node) # get given node path
      meta_type = 'undefined' # instantiate as undefined
      if meta_node: # if its a node in the meta model not in our specific implementation
        AttributeKeys = core.get_attribute_names(node) # attributes of the node, dictionary
        meta_type = core.get_attribute(meta_node, 'name') # get the nodes meta type
        temp['Name'] = name # name of node
        temp['GUID'] = core.get_guid(node) # GUID
        temp['Meta'] = meta_type # type of node
        for x in AttributeKeys:
          att[x] = core.get_attribute(node, x)
        temp['Attributes'] = att # type of node
        D[path] = temp
        if meta_type == 'Place':
          pointer = core.get_collection_names(node) # brings back pointers. eg dst or src
          if pointer[0] == "dst":
            trackfp = core.get_collection_paths(node,'dst')[0]
            insertme = str(name + " | " + trackfp + " | " + "NA")
            #logger.info(insertme)
            ingress.append(insertme)
            allplaces.add(name)
          if pointer[0] == "src":
            FireReq = core.get_attribute(node, 'FireReq') # get the nodes meta type
            trackfp = core.get_collection_paths(node,'src')[0]
            insertme = str(name + " | " + trackfp + " | " + str(FireReq))
            #logger.info(insertme)
            egress.append(insertme)
            allplaces.add(name)
          if len(pointer) > 1:
            if pointer[1] == "src":
              FireReq = core.get_attribute(node, 'FireReq') # get the nodes meta type
              trackfp = core.get_collection_paths(node,'src')[0]
              insertme = str(name + " | " + trackfp + " | " + str(FireReq))
              #logger.info(insertme)
              egress.append(insertme)
              allplaces.add(name)
            
        if meta_type == 'Transition': # two transitions
          pointer = core.get_collection_names(node)
          if pointer[0] == "dst":
            trackfp = core.get_collection_paths(node,'dst')[0]
            insertme = str(name + " | " + trackfp + " | " + "NA")
            ingress.append(insertme)
            allplaces.add(name)
          if pointer[1] == "src":
            trackfp = core.get_collection_paths(node,'src')[0]
            insertme = str(name + " | " + trackfp + " | " + "NA")
            egress.append(insertme)
            allplaces.add(name)
          if pointer[0] == "src":
            trackfp = core.get_collection_paths(node,'src')[0]
            insertme = str(name + " | " + trackfp + " | " + "NA")
            egress.append(insertme)
            allplaces.add(name)
         
          
    self.util.traverse(active_node, traveler)
    D.pop('/4')
    

    AllPath = {}
    RealPath = {}
    
    # Every single possible path into a dictionary
    for x in allplaces:
      for y in allplaces:
        AllPath.update({"{} to {}".format(x,y) : int("-1")})
        
        
    # accessible paths into a dictioanry
    for i in ingress:
      istation = i.split(" | ")[0]
      itrack = i.split(" | ")[1]
      fire = i.split(" | ")[2]
      for e in egress:
        estation = e.split(" | ")[0]
        etrack = e.split(" | ")[1]
        fire = e.split(" | ")[2]
        if itrack == etrack:
          printfriendly = "{} to {} | FireReq {}".format(estation,istation,fire)
          #logger.info(printfriendly)
          RealPath.update({"{} to {}".format(estation,istation) : fire})
          
    fromList = []
    toList = []
    for item in RealPath.items():
      fromList.append(item[0].split(" ")[0])
      toList.append(item[0].split("to ")[1])

     
      
    # check to see if this is a free choice petri net
    if any(fromList.count(element) > 1 for element in fromList):
      self.send_notification('NOT a free choice petri net')
    else:
      self.send_notification('Free Choice Petri Net')
    
    # Check if this is a State machine Petri Net
    if any(fromList.count(element) == 1 for element in fromList):
      if any(toList.count(element) == 1 for element in toList):
        self.send_notification('StateMachine Petri Net')
    else:
      self.send_notification('NOT a StateMachine Petri Net')
      
    # Check if this is a Marked Graph Petri Net
    if any(fromList.count(element) == 1 for element in fromList):
      if any(toList.count(element) == 1 for element in toList):
        self.send_notification('Marked Graph Petri Net')
    else:
      self.send_notification('NOT a Marked Graph Petri Net')
      
    # Check if this is a Worked Flow Petri Net
    toCount = 0
    fromCount = 0
    for x in fromList:
      if x not in toList:
        toCount = toCount + 1
        
    for y in toList:
      if y not in fromList:
        fromCount = fromCount + 1
      
      
    if toCount > 1:
      self.send_notification('NOT a Worked Flow Petri Net')
    
    if fromCount > 1:
      self.send_notification('NOT a Worked Flow Petri Net')
    
      
    json_object = json.dumps(RealPath, indent = 4)
    logger.info(json_object)