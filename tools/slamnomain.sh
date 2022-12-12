perl -0777 -i.original -pe 's/quit:\n    mov rax, 60\n    mov rdi, 0\n    syscall\n//igs' $1
perl -0777 -i.original -pe 's/format ELF64\nsection '"'"'.text'"'"' executable\npublic _start/.text/igs' $1
perl -0777 -i.original -pe 's/_start/kernel_main/igs' $1
perl -0777 -i.original -pe 's/quit/\$kernel_quit/igs' $1
perl -0777 -i.original -pe 's/section '"'"'.bss.*//igs' $1
perl -0777 -i.original -pe 's/section '"'"'.data'"'"'/.section .data/igs' $1
python tools/fasm2as.py $1

if [[ "$2" == "src/kernel/startup.slm" ]]; then
    echo "
kernel_quit:
    ret
.global kernel_main
.global kernel_quit
.bss
.global ret_stack_rsp
ret_stack_rsp: .zero 4, 0x0
.global loc_stack_rsp
loc_stack_rsp: .zero 4, 0x0
.global ret_stack
ret_stack: .zero 1024, 0x0
.global loc_stack
loc_stack: .zero 1024, 0x0
.global mem
mem: .zero 64" >> $1
else
    perl -0777 -i.original -pe 's/jmp kernel_quit\n.*//igs' $1
fi

perl -0777 -i.original -pe 's/    mov %esp,\(args_ptr\)//igs' $1
perl -0777 -i.original -pe 's/ db / .byte /igs' $1

rm $1.original