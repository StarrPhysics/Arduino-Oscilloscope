#include <Arduino.h>

#ifndef ARDUINO_OSCILLOSCOPE_H
#define ARDUINO_OSCILLOSCOPE_H

#define MAX_PINS 10 // Just because I can't dynamically allocate memory in C++. Absolute W

// This macro is used to initalize the ArduinoOscilloscope class. It is used to avoid the need to manually specify the names of each pin. This is intended to be user friendly, so its use is encouraged.
#define InitalizeArduinoOscilloscope(baud, ...) ArduinoOscilloscope(baud, #__VA_ARGS__, __VA_ARGS__)

// ### Use `InitalizeArduinoOscilloscope` to instanciate the class, as it is intended to be user friendly.
// This class is used to create a digital oscilloscope utalizing Ardueno hardware features and a specially designed python client.
class ArduinoOscilloscope {
    public:
        // The constructor for the ArduinoOscilloscope class, which is ran during compile-time.
        template <typename... Args>
        ArduinoOscilloscope(int baud, const char* pinNames, Args... args): _baud(baud), _pinNames(String(pinNames)) {
            processArgs(args...);
        };
        
        void establishConnection();
        void sendPinData();

    private:
        String _pinNames = ""; // A string which a list of the pin names for the oscilloscope program.
        int _pinNumberArray[MAX_PINS]; // An array of the pin numbers.
        int _iterator = 0; // An iterator which is used to iterate through the _pinNumberArray during compile-time. It also is used as a counter for the number of pins stored: '_iterator + 1'.

        bool _connected = false; // A boolean which represents the connection status of Arduino program and the python program.
        int _baud; // The baud rate of the serial bus.
        
        int _bitmask = 0b0001111111; // The bit mask for the first 7 bits of a 10 bit number. The inversion operator (~) is used to obtain the leading 3 bits.

        // This function is used to handle the variable-argument array passed to the constructor resursivly.
        template<typename T, typename... Rest>
        void processArgs(T arg, Rest... rest) {
            _pinNumberArray[_iterator] = arg;
            _iterator += 1;
            processArgs(rest...);
        };
        // This is here because chatgpt told me to lol idk how templates work
        void processArgs() {};
};

#endif // ARDUINO_OSCILLOSCOPE_H
