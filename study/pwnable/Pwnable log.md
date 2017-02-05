

[TOC]

# Pwnable log

```
Pwnable log by muhe@Syclover
```

## 1. Stack Vuln

#### 1.1 Vuln

##### 1.1.1 Stack overflow

##### 1.1.2 Stack Variables uninitialized

##### 1.1.3 off by one

#### 1.2 Tech

##### 1.2.1 ROP

###### [1] Dynamic Linking 

###### [2] Static Linking 

###### [3] x86 && x64

##### 1.2.2 Frame Fake

## 2. Heap Vuln

#### 2.1 Vuln

##### 2.1.1 unsafe unlink (old libc)

##### 2.1.2 off by one

##### 2.1.3 double free

##### 2.1.4 use after free

#### 2.2 Tech

##### 2.2.1 Malloc Maleficarum

###### [1] The House of Prime

###### [2] The House of Mind

###### [3] The House of Force

###### [4] The House of Lore

###### [5] The House of Spirit

##### 2.2.2 unsorted bin unlink(free 'd')

##### 2.2.3 small/large bin unlink(malloc'd)

##### 2.2.4 fastbin dumlicate

##### 2.2.5 hijack function pointer

##### 2.2.6 craft overlapping chunks

##### 2.2.7 heap spray

## 3. Fromat String Vuln

#### 3.1 Vuln

##### 3.1.1 x86

##### 3.1.2 x64

#### 3.2 Tech

###### 3.2.1 leak func addr

###### 3.2.2 dump bin file with fmt

## 4. Other Vuln

#### 4.1 Vuln

##### 4.1.1 Integer overflow

##### 4.1.2 fsp overflow

#### 4.2 Tech

##### 4.2.1 ssp leak

## 5. Some Tricks

#### 5.1 one gadget rce

#### 5.2 canary crack

#### 5.3 canary leak

#### 5.4 bin file dump

#### 5.5 fast confirm libc's version

## 6. Pwn in AD mode

#### 6.1 wapper

#### 6.2 common defence