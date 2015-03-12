# Introduction #

Scintialla autocompletion are the inline popups as soon as a few characters are types.

A file is read (presently, later maybe "coded" load) autocomplete.txt that contains eg
```
myFunction(ping, pong) return a ping to pong
Serial.write()
write(str) writes a string
write(foo, bar, len) writes a string fo foo to bar with a len
```

Note that Serial.write and all the write() are Serial.write() functions, as Scintilla needs the permutations.

So the idea is that the API.Define is loaded from yaml.