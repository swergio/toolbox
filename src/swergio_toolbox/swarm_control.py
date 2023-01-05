import subprocess
import yaml
import time

class Component():
    """
    A class representing a component that can be started and stopped.

    :param filepath: The file path of the component.
    :type filepath: str

    :param projectpath: The project path of the component, if applicable.
    :type projectpath: str

    :param delay: The delay in seconds before starting the component.
    :type delay: int or float

    :param terminal: Whether to start the component in a terminal or not.
    :type terminal: bool

    :ivar filepath: The file path of the component.
    :vartype filepath: str

    :ivar projectpath: The project path of the component, if applicable.
    :vartype projectpath: str

    :ivar delay: The delay in seconds before starting the component.
    :vartype delay: int or float

    :ivar process: The subprocess object representing the running component.
    :vartype process: subprocess.Popen

    :ivar terminal: Whether the component is started in a terminal or not.
    :vartype terminal: bool
    """
    def __init__(self, filepath, projectpath = None, delay = None, terminal = True ):
        self.filepath = filepath
        self.projectpath = projectpath
        self.delay = delay
        self.process = None 
        self.terminal = terminal
        
    def start(self):
        """
        Start the component.
        
        :return: The delay in seconds before starting the component, or None if the file extension is not recognized.
        :rtype: int or float or None
        """
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
        """
        Stop the component.
        """
        if self.process is not None:
            self.process.terminate()

        
class Swarm():
    """
    A class representing a swarm of components that can be started and stopped as a group.

    :param config_file: The file path of the configuration file.
    :type config_file: str

    :ivar config: The configuration for the swarm.
    :vartype config: dict

    :ivar components: The components in the swarm.
    :vartype components: dict
    """
    def __init__(self, config_file = None) -> None:
        """
        Initialize the Swarm.
        
        :param config_file: The file path of the configuration file.
        :type config_file: str
        """
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
        """
        Start the specified components in the swarm.

        :param components: The names of the components to start. If not provided, all components will be started.
        :type components: list of str or str or None

        :return: None
        """
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
        """
        Stop the specified components in the swarm.

        :param components: The names of the components to stop. If not provided, all components will be stopped.
        :type components: list of str or str or None

        :return: None
        """
        if components is None:
            components = list(self.components.keys())
        if isinstance(components,str):
            components = [components]
        for c in components:
            delay = self.components[c].stop()

    
    def add(self,name, filepath,projectpath = None ,delay = None, terminal = True):
        """
        Add a new component to the swarm.

        :param name: The name of the new component.
        :type name: str

        :param filepath: The file path of the new component.
        :type filepath: str

        :param projectpath: The project path of the new component, if applicable.
        :type projectpath: str

        :param delay: The delay in seconds before starting the new component.
        :type delay: int or float

        :param terminal: Whether to start the new component in a terminal or not.
        :type terminal: bool

        :return: None
        """
        self.components[name] = Component(
                filepath,
                projectpath= projectpath,
                delay= delay,
                terminal= terminal
            )

    
    