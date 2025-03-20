from prowl import ProwlStack
from prowl.lib.tool import ProwlTool

from typing import Optional

class Memory:
    pass

class Agent:
    """ Agent Superclass: Each agent has a model and it's own prompt folder"""
    def __init__(self, model:str='qwen/qwen-2.5-7b-instruct', folders:list[str]=['prompts/'], tools:list[ProwlTool]=None):
        self.name = None
        self.model = model
        self.folders = folders
        self.events = {}
        self.tools = tools
        self.memory = None
        self.default_tasks = ['identity', 'recall', 'input', 'think', 'output']
        
    
    def set_token_event(self, event):
        self.events['token_event'] = event
        
    def set_variable_event(self, event):
        self.events['variable_event'] = event
        
    def init_memory(self):
        self.memory = Memory(self.name)
    
    # Stack wrapper / agent.run helper
    
    async def _run(self, 
                  tasks:list[str], 
                  inputs:dict=None, 
                  stops:list[str]=None, 
                  prefix:str=None, 
                  atomic:bool=False, 
                  model:str=None, 
                  verbose:bool=False):
        """ Runs the stack defined by `tasks` """
        stack = ProwlStack(self.folders, silent=not verbose)
        if self.tools is not None:
            stack.add_tools(self.tools)
        stack.__dict__.update(self.events)
        # Set any default inputs if not existing
        if 'context' not in inputs:
            inputs['context'] = 'No additional context.'
        # Default stops
        if stops is None:
            stops = ['\n#', '\n\n\n']
        return await stack.run(tasks, inputs=inputs, stops=stops, model=model or self.model, prefix=prefix, atomic=atomic)
    
    async def run(self,
                  tasks:list[str], 
                  inputs:dict=None, 
                  stops:list[str]=None, 
                  prefix:str=None, 
                  atomic:bool=False, 
                  model:str=None, 
                  verbose:bool=False):
        """ This can be overridden by any subclass as long as it calls `_run` at the end """
        return await self._run(tasks, inputs=inputs, stops=stops, prefix=prefix, atomic=atomic, model=model, verbose=verbose)
