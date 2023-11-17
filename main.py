from sys import argv
from src.memory import memory_alocate 
from src.cpu import cpuChip8
from src.display import display_func

show=display_func()

instance=memory_alocate(argv[1])

filesize=instance.read_rom()
memory=instance.get_mem()

cpuChip8(filesize,memory,show).cycle()