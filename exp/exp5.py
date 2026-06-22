import os
import json  
import time
import imageio as io 
import copy 

from config import Config 

from entity_manager import EntityManager 
from world import World 

from tools.network_manager import NetworkManager
from tools.func_pool import FunctionPool
from tools.genome_operator import GenomeOperator, HaploidOperator
from tools.hyper_encoding import PhenotypeBuilder
from tools.parallel_tool import ParallelTool
from tools.results_manager import ResultsManager
from tools.robot_generator import RobotGenerator
from tools.robot_simulator import RobotSimulator
from tools.substrate import SubstrateBuilder
from tools.distance import DistanceTool

from systems.build_system import BothBuildSystem
from systems.phenotype_system import BothEnvPhenotypeSystem
from systems.evaluation_system import BothEnvEvaluationSystem
from systems.save_gen_system import BothSaveGenSystem
from systems.reproduction_system import BothReproductionSystem
from systems.save_system import BothSaveSystem

def main() :