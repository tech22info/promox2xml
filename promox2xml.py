#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import uuid

if len(sys.argv)==1:
	print ('Укажите имя конфигурационного файла')
else:
	config_f=open(sys.argv[1],'r')
	config=config_f.read()
	config_f.close()
	print ('Преобразование конфигурационного файла: '+sys.argv[1])
	vm_name=''
	ide=[]
	sata=[]
	for line in config.split('\n'):
		param='name:'
		if line[:len(param)]==param:
			vm_name=line.split(param)[1].strip()
		param='bootdisk:'
		if line[:len(param)]==param:
			boot_disk=line.split(param)[1].strip()
		param='cores:'
		if line[:len(param)]==param:
			cores=line.split(param)[1].strip()
		param='memory:'
		if line[:len(param)]==param:
			memory=line.split(param)[1].strip()
		param='sockets:'
		if line[:len(param)]==param:
			socks=line.split(param)[1].strip()
		param='ide'
		if line[:len(param)]==param:
			drive_name=line.split(':')[0]
			drive_path=':'.join(line.split(':')[1:]).strip()
			ide.append([drive_name,drive_path])
		param='sata'
		if line[:len(param)]==param:
			drive_name=line.split(':')[0]
			drive_path=':'.join(line.split(':')[1:]).strip()
			sata.append([drive_name,drive_path])
	ides=''
	for drive in ide:
		if drive[1].split(',')[1]=='media=cdrom':
			ides=ides+"\
    <disk type='block' device='cdrom'>\n\
      <driver name='qemu' type='raw'/>\n\
      <target dev='hdb' bus='ide'/>\n\
      <readonly/>\n\
      <address type='drive' controller='0' bus='0' target='0' unit='1'/>\n\
      <source file='/opt/vm/"+drive[1].split(',')[0].replace(':','_').replace('/','_')+"'/>\n\
    </disk>\n"
	satas=''
	for drive in sata:
		if drive[1].split(',')[1]=='format=qcow2':
			satas=satas+"\
    <disk type='file' device='disk'>\n\
      <driver name='qemu' type='qcow2'/>\n\
      <source file='/opt/vm/"+drive[1].split(',')[0].replace(':','_').replace('/','_')+"'/>\n\
      <target dev='vda' bus='virtio'/>\n\
      <address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0'/>\n\
    </disk>\n"
	xml="<domain type='kvm'>\n\
  <name>"+vm_name+"</name>\n\
  <uuid>"+str(uuid.uuid4())+"</uuid>\n\
  <memory unit='KiB'>"+str(int(memory)*1024)+"</memory>\n\
  <currentMemory unit='KiB'>1048576</currentMemory>\n\
  <cpu mode='custom' match='exact'>\n\
    <model fallback='allow'>Opteron_G2</model>\n\
    <topology sockets='"+socks+"' cores='"+cores+"' threads='1'/>\n\
  </cpu>\n\
  <os>\n\
    <type arch='x86_64' machine='pc-i440fx-utopic'>hvm</type>\n\
    <boot dev='hd'/>\n\
  </os>\n\
  <features>\n\
    <acpi/>\n\
    <apic/>\n\
    <pae/>\n\
  </features>\n\
  <cpu mode='custom' match='exact'>\n\
    <model fallback='allow'>Opteron_G2</model>\n\
  </cpu>\n\
  <clock offset='utc'>\n\
    <timer name='rtc' tickpolicy='catchup'/>\n\
    <timer name='pit' tickpolicy='delay'/>\n\
    <timer name='hpet' present='no'/>\n\
  </clock>\n\
  <on_poweroff>destroy</on_poweroff>\n\
  <on_reboot>restart</on_reboot>\n\
  <on_crash>restart</on_crash>\n\
  <pm>\n\
    <suspend-to-mem enabled='no'/>\n\
    <suspend-to-disk enabled='no'/>\n\
  </pm>\n\
  <devices>\n\
    <emulator>/usr/bin/kvm-spice</emulator>\n\
"+satas+ides+"\
    <interface type='network'>\n\
      <mac address='52:54:00:ac:e4:8f'/>\n\
      <source network='default'/>\n\
      <model type='virtio'/>\n\
      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>\n\
    </interface>\n\
    <input type='mouse' bus='ps2'/>\n\
    <input type='keyboard' bus='ps2'/>\n\
    <graphics type='spice' autoport='yes'/>\n\
    <sound model='ich6'>\n\
      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>\n\
    </sound>\n\
    <video>\n\
      <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1'/>\n\
      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>\n\
    </video>\n\
    <redirdev bus='usb' type='spicevmc'>\n\
    </redirdev>\n\
    <redirdev bus='usb' type='spicevmc'>\n\
    </redirdev>\n\
    <redirdev bus='usb' type='spicevmc'>\n\
    </redirdev>\n\
    <redirdev bus='usb' type='spicevmc'>\n\
    </redirdev>\n\
    <memballoon model='virtio'>\n\
      <address type='pci' domain='0x0000' bus='0x00' slot='0x09' function='0x0'/>\n\
    </memballoon>\n\
  </devices>\n\
</domain>"
#	print ('XML-файл конфигурации:'+xml)
	print ('Имя виртуальной машины: '+vm_name)
	print ('Загрузочный диск: '+boot_disk)
	print ('Объем памяти: '+memory)
	print ('Сокетов: '+socks+' / Ядер: '+cores)
	print ('IDE-диски: '+str(ide))
	print ('SATA-диски: '+str(sata))
	config_f=open(sys.argv[1]+'.xml','w')
	config_f.write(xml)
	config_f.close()
