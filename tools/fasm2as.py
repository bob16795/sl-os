import sys
import re

result = ""
curproc = ""

tab = {
  "[loc_stack]": "(loc_stack)",
  "loc_stack": "$loc_stack",
  "[loc_stack_rsp]": "(loc_stack_rsp)",
  "loc_stack_rsp": "$loc_stack_rsp",
  "[ret_stack]": "(ret_stack)",
  "ret_stack": "$ret_stack",
  "[ret_stack_rsp]": "(ret_stack_rsp)",
  "ret_stack_rsp": "$ret_stack_rsp",
  "[args_ptr]": "(args_ptr)",
  "args_ptr": "$args_ptr",
  "rax": "%eax",
  "[rax]": "(%eax)",
  "[rax - 8]": "-8(%eax)",
  "rbx": "%ebx",
  "[rbx]": "(%ebx)",
  "rcx": "%ecx",
  "[rcx]": "(%ecx)",
  "rdx": "%edx",
  "[rdx]": "(%edx)",
  "rsp": "%esp",
  "bl": "%bl",
  "al": "%al",
  "dx": "%dx",
}

with open(sys.argv[1], "r") as file:
  for line in file.readlines():
    if ";" in line:
      line = line.split(";")[0] + "\n"
    line = line.replace(" qword", "")
    line = line.replace(" byte", "")
    line = line.replace("'", "")

    if line.strip() == "":
      continue
    elif len(line) > 3 and line.strip()[0:3] == "str":
      result += "    " + line
      continue
    elif line.strip()[0] == "." and line.strip()[-1] == ":":
      line = curproc + line
      result += line
      continue
    elif line.strip()[0] == ".":
      result += line
      continue
    elif line.strip()[-1] == ":":
      curproc = line.strip()[:-1]
      result += ".global " + curproc + "\n"
      result += line
      continue

    cmd = line.strip().split(" ")[0].strip()
    params = " ".join(line.strip().split(" ")[1:]).split(",")

    for p in range(len(params)):
      if re.match(r"^[0-9]+$", params[p].strip()):
        params[p] = " $" + params[p].strip()
      elif re.match(r"^[\dA-F]+h$", params[p].strip()):
        params[p] = "0x" + params[p].strip()[:-1]
        print(params[p])
      elif params[p].strip() == "": 
        pass
      elif params[p].strip()[0] == ".":
        params[p] = curproc + params[p].strip()
      params[p] = tab.get(params[p].strip(), params[p].strip()).strip()
    
    params.reverse()
      
    line = "    " + cmd + " " + ",".join(params) + "\n"

    line = line.replace("jmp (%eax)", "mov (%eax),%ebx\n    jmp *%ebx")
    line = line.replace("jmp $", "jmp ")
    line = line.replace("add $8,%esp", "pop %eax")
    line = line.replace("push str", "push $str")

    if re.match(r"^    push mem", line):
      result += "    mov $mem,%eax\n"
      result += "    add $" + line[13:-1] + ",%eax\n"
      result += "    push %eax\n"
    elif re.match(r"^    mov proc_.*,\(%eax\)", line):
      result += line.replace(",(%eax)", ",%ebx").replace("mov ", "mov $")
      result += "    mov %ebx,(%eax)\n"
    else:
      result += line.replace(
        "mov %bl,%ebx", "movb %bl,(%ebx)")

result = result.replace("mov $ret_stack,(ret_stack_rsp)\n    mov (ret_stack_rsp),%eax", "mov $ret_stack,%eax\n    mov %eax,(ret_stack_rsp)")

with open(sys.argv[1], "w") as file:
  file.write(result)