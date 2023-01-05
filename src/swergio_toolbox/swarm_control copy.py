import subprocess
import yaml
import time

class Component():
    
    def __init__(self, filepath, projectpath = None, delay = None, terminal = True ):
        self.filepath = filepath
        self.projectpath = projectpath
        self.delay = delay
        self.process = None 
        self.terminal = terminal
        
    def start(self):
        if self.filepath.split('.')[-1] == "py":
            lang = "python3"
        elif self.filepath.split('.')[-1] == "jl":
            lang = "julia"
        else:
            return None
        
        if self.projectpath is not None and lang == "julia":
            if self.projectpath == ".":
                cmd = [lang,"--project","-i",self.filepath]
            else:
                cmd = [lang,"--project",self.projectpath,"-i",self.filepath]
        else:
            cmd = [lang,"-i",self.filepath]
        
        if self.terminal:
            command = ["xterm", "-fs",  "14", "-fa", "DejaVuSansMono", "-hold", "-e"] + cmd
        else:
            command = cmd
        self.process = subprocess.Popen(command)
        
        return self.delay    

    def stop(self):
        if self.process is not None:
            self.process.terminate()
        
class Swarm():
    
    def __init__(self, config_file = None) -> None:
        if config_file is None:
            config_file = 'swarm.yaml'
        with open(config_file, 'r') as stream:
            self.config = yaml.safe_load(stream)
        self.components = {}
        for k,v in self.config['components'].items():
            self.components[k] = Component(
                v['filepath'],
                projectpath= v['projectpath'] if 'projectpath' in v.keys() else None,
                delay= v['delay'] if 'delay' in v.keys() else None,
                terminal= v['terminal'] if 'terminal' in v.keys() else True
            )
        
        
    def start(self, components = None):
        if components is None:
            components = list(self.components.keys())
        if isinstance(components,str):
            components = [components]
        for c in components:
            delay = self.components[c].start()
            if delay is not None:
                print("DELAY")
                time.sleep(delay)
            
    def stop(self, components = None):
        if components is None:
            components = list(self.components.keys())
        if isinstance(components,str):
            components = [components]
        for c in components:
            delay = self.components[c].stop()
    
    def add(self,name, filepath,projectpath = None ,delay = None, terminal = True):
        self.components[name] = Component(
                filepath,
                projectpath= projectpath,
                delay= delay,
                terminal= terminal
            )
    
    