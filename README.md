# xss-scanner
Script para encontrar las posibles vulnerabilidades XSS de tipo Reflejado en páginas web.

![Muestra del script](https://github.com/juliospau/xss-scanner/blob/main/muestraScript.PNG)
![Muestra 2 del script](https://github.com/juliospau/xss-scanner/blob/main/muestraScript-2.PNG)

Nota: se puede modificar el payload para descubrir vulnerabilidades de tipo RCE. Ejemplo: se puede modificar a 'test; ls -lha' para listar ficheros y directorios del servidor empleando la misma web de prueba en este caso 'Mutillidae' en 'Metasploitable 2' y contra el endpoint 'dns-lookup.php' -> http://10.0.2.27/mutillidae/index.php?page=dns-lookup.php.

Pte. Añadir más capacidades.
