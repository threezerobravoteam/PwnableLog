#!/usr/bin/env python
# coding=utf-8
# author:muhe
# based on http://uaf.io/exploitation/misc/2016/04/02/Finding-Functions.html

class MyDynELF(object):
	"""docstring for MyDynELF"""
	def __init__(self, BITS = 64):
		self.BITS = 64

	# leak arbitrary func addr
	def get_elf_entry(self, got,leak):
        entry = u64(leak(got, 0x8))
        print '[+]Libc entry : 0x%x' % entry
        return entry

	#get libc base addr
	def get_elf_base(self,entry,leak):
		entry = u64(entry)
		libc_base = entry & 0xfffffffffffff000
		if self.BITS == 64:
			while True:
				tmp = leak(libc_base,0x8)
				if tmp[0:4] == '\x7fELF':
					break
				libc_base -= 0x1000
			print '[+]Libc base : 0x%x' % (libc_base)
			return libc_base
		else:
			#not support now
			return 0

	#get program header addr
	def find_Phdr(self,addr,leak):
		if self.BITS == 64:
			e_phoff = u64(leak(addr + 0x20,0x8).ljust(8, '\0'))
		else:
			e_phoff = u32(leak(addr + 0x1c,0x4).ljust(4, '\0'))
		print '[+]Program header : 0x%x' % (e_phoff + addr)
		return e_phoff + addr

	#get DYNAMIC section
	def findDynamic(,self,Phaddr,elf_base,leak):
		if self.BITS == 64:
			i = -56
			p_type = 0
			while p_type != 2:
				i+=56
				p_type = u32(leak(Phaddr + i,0x4))
			dynamic_addr = u64(leak(Phaddr+i+16,0x8)) + elf_base
			print "[+]Dynamic addr 0x%x" % (dynamic_addr)
			return dynamic_addr
		else:
			#not support now
			return 0

	# find PIE
	def findIfPIE(self,addr,leak):
		e_type = u8(leak(addr + 0x10,0x8)[:1])
		if e_type == 3:
			printn "[+]PIE enable"
			return addr
		else:
			return 0

	# find DT_STRTAB and DT_SYMTAB
	def findDynTable(self,DynamicAddr,leak):
		# for DT_STRTAB -- 5
		# for DT_SYMTAB -- 6
		tmp_dyn = DynamicAddr
		dt_sym_addr = 0
		dt_str_addr = 0
		while True:
			garbage = u64(leak(tmp_dyn,0x8))
			if garbage == 0x6:
				dt_sym_addr = u64(leak(tmp_dyn + 0x8,0x8))
			elif garbage == 0x5:
				dt_str_addr = u64(leak(tmp_dyn + 0x8,0x8))
			if dt_str_addr and dt_sym_addr:
				break;
			tmp_dyn += 0x10
		print "[+]DT_STRTAB at : 0x%x\n[+]DT_SYMTAB at : 0x%x" % (dt_str_addr,dt_sym_addr)
		return (dt_sym_addr,dt_str_addr)

	# find func you want
	def findSymbol(self,strtab,symtab,symbol,elf_base,leak):
		tmp_sym = symtab
		while True:
			garbage = u32(leak(tmp_sym,0x4))
			name = leak(strtab+garbage,len(symbol))
			if name == symbol:
				break
			tmp_sym += 0x18
		symbol_addr = u64(leak(tmp_sym+0x8,0x8)) + elf_base
		print "[+]Got func : 0x%x" % (symbol_addr)
		return symbol_addr

	 def lookup(self, leak, ptr, symbol):
        entry                   = self.get_elf_entry(ptr, leak)
        elf_base                = self.get_elf_base(entry, leak)
        phdr                    = self.find_Phdr(elf_base, leak)
        dyn_section             = self.findDynamic(phdr, elf_base, leak)
        dt_sym_tab, dt_str_tab  = self.findDynTable(dyn_section, leak)
        func_address            = self.findSymbol(dt_sym_tab, dt_str_tab, symbol, elf_base, leak)
        return func_address