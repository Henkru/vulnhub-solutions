level1@pb0x:~$ objdump --dynamic-reloc level2 |grep free
0x0804a378 R_386_JUMP_SLOT   free

typedef struct {
	int len;
	char* text;
} Note;

Note *create_struct()
{
  Note *note = malloc(8);
  note->len = 64;
  note->text = malloc(64);
  mprotect(note->text & 0xfffff000, note->len, PROT_READ | PROT_WRITE | PROT_EXEC);
  return note;
}

int __cdecl slot_exists(int a1, int a2)
{
  int result; // eax@2

  if ( a2 <= list_size )
    result = *(_DWORD *)(4 * a2 + a1) != 0;
  else
    result = 0;
  return result;
}

//Writepart
else if ( !strcmp(&text, "set") )
{
  readline(&text, 0x80u, "> id: ", 10);
  slotNum = strtol(&text, 0, 10);
  if ( slot_exists(notes, slotNum) == 1 )
  {
    readline(&text, 0x80u, "> text(32 max): ", 0);
    Note *note = notes[slotNum];
    note->len = strlen(&text);
    memcpy(note->text, &text, note->len);

    printf("[*] Note %d set\n", slotNum);
  }
  else
  {
    printf("[!] Note id %d doesnt exist\n", slotNum);
  }
}
