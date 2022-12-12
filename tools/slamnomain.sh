perl -0777 -i.original -pe 's/quit:\n    mov rax, 60\n    mov rdi, 0\n    syscall\n.*//igs' $1
perl -0777 -i.original -pe 's/format ELF64\nsection '"'"'.text'"'"' executable\npublic _start/.text/igs' $1
perl -0777 -i.original -pe 's/_start/kernel_main/igs' $1
perl -0777 -i.original -pe 's/quit/\$kernel_quit/igs' $1
python tools/fasm2as.py $1

echo "
kernel_quit:
    ret
.global kernel_main
.section .data
str_0:
    .string \"Hello World!\"
    .zero 1
.bss
ret_stack_rsp: .zero 4, 0x0
loc_stack_rsp: .zero 4, 0x0
ret_stack: .zero 1024, 0x0
loc_stack: .zero 1024, 0x0
mem: .zero 64" >> $1


perl -0777 -i.original -pe 's/    mov %esp,\(args_ptr\)//igs' $1

rm $1.original