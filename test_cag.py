
from database import get_machine_context

machine_id = "M101"

context = get_machine_context(machine_id)

print("\n===== CAG MACHINE CONTEXT =====\n")
print(context)
