#include <Arduino.h>
using namespace std;

#ifndef ARDUINO_OSCILLOSCOPE_H
#define ARDUINO_OSCILLOSCOPE_H
#define MAX_PINS 10 // Just because I can't dynamically allocate memory in C++. Absolute W
#define InitalizeArduinoOscilloscope(baud, ...) ArduinoOscilloscope(baud, #__VA_ARGS__, __VA_ARGS__)

class ArduinoOscilloscope {
    public:
        template <typename... Args>
        ArduinoOscilloscope(int baud, const char* pinNames, Args... args): _baud(baud), _pinNames(String(pinNames)) {
            
            processArgs(0, args...);
        };
        
        void establishConnection();
        void sendPinData();

    private:
        int _pins[MAX_PINS];
        String _pinNames = "";
        int _baud;

        template<typename T, typename... Rest>
        void processArgs(int i, T arg, Rest... rest);
        void processArgs();

};

#endif // ARDUINO_OSCILLOSCOPE_H
