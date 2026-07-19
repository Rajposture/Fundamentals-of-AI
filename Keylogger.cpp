#include <fstream>
#include <ctime>
#include <conio.h>
#include <cctype>
#include <string>
#include <iomanip>
static std::string now() {
char buf[20];
std::time_t t = std::time(nullptr);
std::strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", std::localtime(&t));
return std::string(buf);
}
static std::string key_repr(unsigned char ch) {
if (ch == 0x1B) return "<ESC>";
if (ch == '\n') return "<LF>";
if (ch == '\r') return "<CR>";
if (ch == '\t') return "<TAB>";
if (ch == ' ') return "' '";
if (std::isprint(ch)) return std::string("'") + std::string(1, static_cast<char>(ch)) + "'";
return "'?'";
}
int main() {
std::ofstream out("keystrokes.log", std::ios::app);
if (!out) return 1;
out << "=== New session: " << now() << " ===\n";
while (true) {
int ch = _getch(); // waits for key, no echo
unsigned char uch = static_cast<unsigned char>(ch);
if (ch == 0 || ch == 0xE0) { // special keys (arrows, fn keys...)
int ch2 = _getch();
out << "[" << now() << "] <SPECIAL 0x"
<< std::hex << std::setw(2) << std::setfill('0') << (ch2 & 0xFF)
<< std::dec << ">\n";
out.flush();
continue;
}
std::string repr = key_repr(uch);
out << "[" << now() << "] " << repr
<< " (0x" << std::hex << std::setw(2) << std::setfill('0') << int(uch)
<< std::dec << ")\n";
out.flush();
if (repr == "<ESC>") {
out << "=== Session closed: " << now() << " ===\n\n";
break;
}
}
return 0;
}