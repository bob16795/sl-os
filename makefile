default: disk.iso

clean:
	rm -f obj/kernel.o
	rm -f obj/kernel/tty.o

obj/boot.o: src/boot.s
	i686-elf-as src/boot.s -o obj/boot.o

obj/%.o: src/%.slm
	rm -f $<.asm
	slam -a -o $< $<
	tools/slamnomain.sh $<.asm
	i686-elf-as $<.asm -o $@
	rm $<.asm

disk.bin: linker.ld obj/boot.o obj/kernel.o
	i686-elf-gcc -T linker.ld -o disk.bin -ffreestanding -O2 -nostdlib obj/boot.o obj/kernel.o -lgcc

disk.iso: disk.bin tools/grub.cfg
	mkdir -p isodir
	mkdir -p isodir/boot/grub
	cp disk.bin isodir/boot/disk.bin
	cp tools/grub.cfg isodir/boot/grub/grub.cfg
	grub-mkrescue -o disk.iso isodir
