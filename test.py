from deepspeed import init_distributed
from mpi4py import MPI

init_distributed(dist_backend="mpi")
print("DeepSpeed and MPI are working!")